from flask.views import MethodView
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required
from project.config import WINGMAN_PRJ_DIR, INTENTS_FILE_NAME
from pathlib import Path
from project import util
import json

prj_root = Path(WINGMAN_PRJ_DIR)


class IntentsAPI(MethodView):
    """Wingman Intents API"""

    @jwt_required()
    def get(self, project_name, intent_name):
        """
            intent_name
                None: Retrieve All Intent Names
                An intent name: Get An intent
        """
        if intent_name:
            try:
                util.check_name(project_name)

                intents_file = prj_root.joinpath(
                    project_name, 'intents', INTENTS_FILE_NAME)

                with open(intents_file, 'r', encoding="utf-8") as json_file:
                    intents_json = json.load(json_file)

                intent = intents_json[intent_name]
            except Exception as e:
                response = jsonify({'msg': str(e)})
                return response, 400
            else:
                return jsonify(intent), 200
        else:
            try:
                util.check_name(project_name)

                intents_file = prj_root.joinpath(
                    project_name, 'intents', INTENTS_FILE_NAME)

                with open(intents_file, 'r', encoding="utf-8") as json_file:
                    intents_json = json.load(json_file)
            except Exception as e:
                response = jsonify({'msg': str(e)})
                return response, 400
            else:
                return jsonify({'intent_name': list(intents_json.keys())}), 200

    @jwt_required()
    def post(self, project_name):
        """Create An intent"""

        try:
            intent_name = request.json.get('intent_name', None)

            util.check_name(project_name)
            
            # check intent_name
            if intent_name is None:
                raise ValueError('Missing Intent Name')
            
            intents_file = prj_root.joinpath(
                project_name, 'intents', INTENTS_FILE_NAME)

            with open(intents_file, 'r', encoding="utf-8") as json_file:
                intents_json = json.load(json_file)

            # check intent_name
            if intent_name in intents_json:
                raise ValueError('Intent already exist')

            intents_json[intent_name] = None
            with open(intents_file, 'w', encoding="utf-8") as json_file:
                json.dump(intents_json, json_file, indent=4)
        except Exception as e:
            response = jsonify({'msg': str(e)})
            return response, 400
        else:
            response = jsonify({"msg": "OK"})
            return response, 200

    @jwt_required()
    def put(self, project_name, intent_name):
        """Update A Intent"""

        try:
            body = request.json

            util.check_name(project_name)

            intents_file = prj_root.joinpath(
                project_name, 'intents', INTENTS_FILE_NAME)

            with open(intents_file, 'r', encoding="utf-8") as json_file:
                intents_json = json.load(json_file)

            intents_json[intent_name] = body

            with open(intents_file, 'w', encoding="utf-8") as json_file:
                json.dump(intents_json, json_file, indent=4)
        except Exception as e:
            response = jsonify({"msg": str(e)})
            return response, 400
        else:
            response = jsonify({"msg": "OK"})
            return response, 200

    @jwt_required()
    def delete(self, project_name, intent_name):
        """Delete A Project"""

        try:
            util.check_name(project_name)

            intents_file = prj_root.joinpath(
                project_name, 'intents', INTENTS_FILE_NAME)

            with open(intents_file, 'r', encoding="utf-8") as json_file:
                intents_json = json.load(json_file)

            del intents_json[intent_name]

            with open(intents_file, 'w', encoding="utf-8") as json_file:
                json.dump(intents_json, json_file, indent=4)
        except Exception as e:
            response = jsonify({"msg": str(e)})
            return response, 400
        else:
            response = jsonify({"msg": "OK"})
            return response, 200


def init(app: Flask):

    intents_view = IntentsAPI.as_view('intents_api')
    app.add_url_rule('/projects/<string:project_name>/intents',
                     defaults={'intent_name': None}, view_func=intents_view, methods=['GET'])
    app.add_url_rule('/projects/<string:project_name>/intents', view_func=intents_view,
                     methods=['POST'])
    app.add_url_rule('/projects/<string:project_name>/intents/<string:intent_name>',
                     view_func=intents_view, methods=['GET', 'PUT', 'DELETE'])
