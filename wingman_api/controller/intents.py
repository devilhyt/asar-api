from flask.views import MethodView
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required
from wingman_api.config import WINGMAN_PRJ_DIR, INTENTS_FILE_NAME, INTENT_KEYS, INTENT_KEYS_ADDED
from pathlib import Path
from wingman_api import util
import json

prj_root = Path(WINGMAN_PRJ_DIR)


class IntentsAPI(MethodView):
    """Wingman Intents API"""

    @jwt_required()
    def get(self, project_name, intent_name):
        """
        :param intent_name:
            If intent_name is None, then Retrieve All Intent Names.\n
            If intent_name is not None, then Get An intent.
        """
        try:
            if intent_name:
                # Validity check
                util.check_name(project_name)

                # Implement
                intents_file = prj_root.joinpath(
                    project_name, 'intents', INTENTS_FILE_NAME)
                with open(intents_file, 'r', encoding="utf-8") as json_file:
                    intents_json = json.load(json_file)

                intent_obj = intents_json[intent_name]

                return jsonify(intent_obj), 200
            else:
                # Validity check
                util.check_name(project_name)

                # Implement
                intents_file = prj_root.joinpath(
                    project_name, 'intents', INTENTS_FILE_NAME)
                with open(intents_file, 'r', encoding="utf-8") as json_file:
                    intents_json = json.load(json_file)

                return jsonify({'intent_name': list(intents_json.keys())}), 200
        except Exception as e:
            response = jsonify({'msg': str(e)})
            return response, 400

    @jwt_required()
    def post(self, project_name):
        """Create An intent"""

        try:
            intent_name = request.json.get('intent_name', None)

            # Validity check
            util.check_name(project_name)
            if intent_name is None:
                raise ValueError('Missing Intent Name')

            intents_file = prj_root.joinpath(
                project_name, 'intents', INTENTS_FILE_NAME)
            with open(intents_file, 'r', encoding="utf-8") as json_file:
                intents_json = json.load(json_file)

            if intent_name in intents_json:
                raise ValueError('Intent already exist')

            # Implement
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
        """Update An Intent"""
        
        try:
            content = request.json
            new_intent_name = content.pop('new_intent_name', None)
            
            # Validity check
            util.check_name(project_name)
            util.check_key(INTENT_KEYS + INTENT_KEYS_ADDED, content)

            intents_file = prj_root.joinpath(
                project_name, 'intents', INTENTS_FILE_NAME)
            with open(intents_file, 'r', encoding="utf-8") as json_file:
                intents_json = json.load(json_file)
            
            if intent_name not in intents_json:
                raise ValueError('Intent does not exist')
            elif new_intent_name:
                if new_intent_name in intents_json:
                    raise ValueError('Duplicate names are not allowed')
            
            # Implement
            if content:
                intents_json[intent_name] = content
            if new_intent_name:
                intents_json[new_intent_name] = intents_json.pop(intent_name)
                
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
        """Delete An Intent"""

        try:
            # Validity check
            util.check_name(project_name)
            
            # Implement
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
                     defaults={'intent_name': None}, 
                     view_func=intents_view, 
                     methods=['GET'])
    app.add_url_rule('/projects/<string:project_name>/intents', 
                     view_func=intents_view,
                     methods=['POST'])
    app.add_url_rule('/projects/<string:project_name>/intents/<string:intent_name>',
                     view_func=intents_view, 
                     methods=['GET', 'PUT', 'DELETE'])
