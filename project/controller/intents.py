from flask.views import MethodView
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required
from project.config import WINGMAN_PRJ_DIR
from pathlib import Path
from project import util
import json

prj_root = Path(f'{WINGMAN_PRJ_DIR}')


class IntentsAPI(MethodView):
    """Wingman Intents API"""

    @jwt_required()
    def get(self, projectName, intentName=None):
        """
            intentName
                None: Retrieve All Intent Names
                An intent name: Get An intent
        """
        if intentName:
            try:
                util.check_name(projectName)
                util.check_name(intentName)

                intents_file = prj_root.joinpath(
                    projectName, 'intents', 'intents.json')
                
                with open(intents_file, 'r', encoding="utf-8") as json_file:
                    intents_json = json.load(json_file)
                    
                intent = intents_json[intentName]
            except Exception as e:
                response = jsonify({'msg': str(e), 'projectName': projectName})
                return response, 400
            else:
                return jsonify(intent), 200
        else:
            try:
                util.check_name(projectName)

                intents_file = prj_root.joinpath(
                    projectName, 'intents', 'intents.json')

                with open(intents_file, 'r', encoding="utf-8") as json_file:
                    intents_json = json.load(json_file)
            except Exception as e:
                response = jsonify({'msg': str(e), 'projectName': projectName})
                return response, 400
            else:
                return jsonify({'intentName': list(intents_json.keys()), 'projectName': projectName}), 200

    @jwt_required()
    def post(self, projectName):
        """Create An intent"""

        try:
            intentName = request.json.get('intentName', None)

            util.check_name(projectName)
            util.check_name(intentName)

            intents_file = prj_root.joinpath(
                projectName, 'intents', 'intents.json')

            with open(intents_file, 'r', encoding="utf-8") as json_file:
                intents_json = json.load(json_file)

            if intentName not in intents_json:
                intents_json[intentName] = None
            else:
                raise ValueError('Intent already exist')

            with open(intents_file, 'w', encoding="utf-8") as json_file:
                json.dump(intents_json, json_file, indent=4)
        except Exception as e:
            response = jsonify(
                {'msg': str(e), 'projectName': projectName, 'intentName': intentName})
            return response, 400
        else:
            response = jsonify(
                {"msg": "OK", "projectName": projectName, 'intentName': intentName})
            return response, 200

    @jwt_required()
    def put(self, projectName, intentName):
        """Update A Intent"""

        try:
            body = request.json

            util.check_name(projectName)
            util.check_name(intentName)

            intents_file = prj_root.joinpath(
                projectName, 'intents', 'intents.json')

            with open(intents_file, 'r', encoding="utf-8") as json_file:
                intents_json = json.load(json_file)

            intents_json[intentName] = body

            with open(intents_file, 'w', encoding="utf-8") as json_file:
                json.dump(intents_json, json_file, indent=4)
        except Exception as e:
            response = jsonify(
                {"msg": str(e), "projectName": projectName, 'intentName': intentName})
            return response, 400
        else:
            response = jsonify(
                {"msg": "OK", "projectName": projectName, 'intentName': intentName})
            return response, 200

    @jwt_required()
    def delete(self, projectName, intentName):
        """Delete A Project"""

        try:
            util.check_name(projectName)
            util.check_name(intentName)

            intents_file = prj_root.joinpath(
                projectName, 'intents', 'intents.json')

            with open(intents_file, 'r', encoding="utf-8") as json_file:
                intents_json = json.load(json_file)

            del intents_json[intentName]

            with open(intents_file, 'w', encoding="utf-8") as json_file:
                json.dump(intents_json, json_file, indent=4)
        except Exception as e:
            response = jsonify(
                {"msg": str(e), "projectName": projectName, 'intentName': intentName})
            return response, 400
        else:
            response = jsonify(
                {"msg": "OK", "projectName": projectName, 'intentName': intentName})
            return response, 200


def init(app: Flask):

    intents_view = IntentsAPI.as_view('intents_api')
    app.add_url_rule('/projects/<string:projectName>/intents', view_func=intents_view,
                     methods=['GET', 'POST'])
    app.add_url_rule('/projects/<string:projectName>/intents/<string:intentName>',
                     view_func=intents_view, methods=['GET', 'PUT', 'DELETE'])
