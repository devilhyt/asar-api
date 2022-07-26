from flask.views import MethodView
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required
from project.config import WINGMAN_PRJ_DIR, ACTIONS_FILE_NAME, ACTION_KEYS, ACTION_KEYS_ADDED, WINGMAN_ROOT
from pathlib import Path
from project import util
import json

prj_root = Path(WINGMAN_PRJ_DIR)
actions_root = Path(WINGMAN_ROOT, 'project', 'assets', 'actions')


class ActionsAPI(MethodView):
    """Wingman Actions API"""

    @jwt_required()
    def get(self, project_name, action_name):
        """
        :param action_name:
            If action_name is None, then retrieve all action names.\n
            If action_name is not None, then get an action.
        """
        try:
            if action_name:
                # Validity check
                util.check_name(project_name)

                # Implement
                actions_file = prj_root.joinpath(
                    project_name, 'actions', ACTIONS_FILE_NAME)
                with open(actions_file, 'r', encoding="utf-8") as json_file:
                    actions_json = json.load(json_file)

                action_obj = actions_json[action_name]

                return jsonify(action_obj), 200
            else:
                # Validity check
                util.check_name(project_name)

                # Implement
                actions_file = prj_root.joinpath(
                    project_name, 'actions', ACTIONS_FILE_NAME)
                with open(actions_file, 'r', encoding="utf-8") as json_file:
                    actions_json = json.load(json_file)

                return jsonify({'action_name': list(actions_json.keys())}), 200
        except Exception as e:
            response = jsonify({'msg': str(e)})
            return response, 400

    @jwt_required()
    def post(self, project_name):
        """Create An action"""

        try:
            content = request.json
            action_name = content.pop('action_name', None)

            # Validity check
            util.check_name(project_name)
            if action_name is None:
                raise ValueError('Missing Action Name')

            actions_file = prj_root.joinpath(
                project_name, 'actions', ACTIONS_FILE_NAME)
            with open(actions_file, 'r', encoding="utf-8") as json_file:
                actions_json = json.load(json_file)

            if action_name in actions_json:
                raise ValueError('Action already exist')

            # Implement
            actions_json[action_name] = content
            with open(actions_file, 'w', encoding="utf-8") as json_file:
                json.dump(actions_json, json_file, indent=4)
        except Exception as e:
            response = jsonify({'msg': str(e)})
            return response, 400
        else:
            response = jsonify({"msg": "OK"})
            return response, 200

    @jwt_required()
    def put(self, project_name, action_name):
        """Update A Intent"""

        try:
            content = request.json
            new_action_name = content.pop('new_action_name', None)

            # Validity check
            util.check_name(project_name)
            util.check_key(ACTION_KEYS + ACTION_KEYS_ADDED, content)

            actions_file = prj_root.joinpath(
                project_name, 'actions', ACTIONS_FILE_NAME)
            with open(actions_file, 'r', encoding="utf-8") as json_file:
                actions_json = json.load(json_file)

            if action_name not in actions_json:
                raise ValueError('Action does not exist')
            elif new_action_name:
                if new_action_name in actions_json:
                    raise ValueError('Duplicate names are not allowed')

            # Implement
            if content:
                actions_json[action_name] = content
            if new_action_name:
                actions_json[new_action_name] = actions_json.pop(action_name)

            with open(actions_file, 'w', encoding="utf-8") as json_file:
                json.dump(actions_json, json_file, indent=4)
        except Exception as e:
            response = jsonify({"msg": str(e)})
            return response, 400
        else:
            response = jsonify({"msg": "OK"})
            return response, 200

    @jwt_required()
    def delete(self, project_name, action_name):
        """Delete A Project"""

        try:
            # Validity check
            util.check_name(project_name)

            # Implement
            actionss_file = prj_root.joinpath(
                project_name, 'actions', ACTIONS_FILE_NAME)
            with open(actionss_file, 'r', encoding="utf-8") as json_file:
                actions_json = json.load(json_file)

            del actions_json[action_name]
            with open(actionss_file, 'w', encoding="utf-8") as json_file:
                json.dump(actions_json, json_file, indent=4)
        except Exception as e:
            response = jsonify({"msg": str(e)})
            return response, 400
        else:
            response = jsonify({"msg": "OK"})
            return response, 200


class ActionTypeAPI(MethodView):
    """Wingman Action Type API"""

    @jwt_required()
    def get(self):
        """Get the names of all action types"""

        # Implement
        type_names = [d.stem for d in actions_root.iterdir() if d.is_dir()]
        return jsonify({'type_names': type_names})
    
class ActionSchemaAPI(MethodView):
    """Wingman Action Schema API"""

    @jwt_required()
    def get(self, type_name):
        """Get the schema of an action type"""
        try:
            type_names = [d.stem for d in actions_root.iterdir() if d.is_dir()]
            if type_name not in type_names:
                raise ValueError('Action type does not exist')

            schema_file = actions_root.joinpath(type_name, 'schema.json')
            
            # Implement
            with open(schema_file, 'r', encoding="utf-8") as json_file:
                schema_json = json.load(json_file)
            
        except Exception as e:
            response = jsonify({"msg": str(e)})
            return response, 400
        else:
            response = jsonify(schema_json)
            return response, 200


def init(app: Flask):

    actions_view = ActionsAPI.as_view('actions_api')
    app.add_url_rule('/projects/<string:project_name>/actions',
                     defaults={'action_name': None}, view_func=actions_view, methods=['GET'])
    app.add_url_rule('/projects/<string:project_name>/actions', view_func=actions_view,
                     methods=['POST'])
    app.add_url_rule('/projects/<string:project_name>/actions/<string:action_name>',
                     view_func=actions_view, methods=['GET', 'PUT', 'DELETE'])

    action_type_view = ActionTypeAPI.as_view('action_type_api')
    app.add_url_rule('/actions/types',
                     view_func=action_type_view, methods=['GET'])
    
    action_schema_view = ActionSchemaAPI.as_view('action_schema_api')
    app.add_url_rule('/actions/schema/<string:type_name>',
                     view_func=action_schema_view, methods=['GET'])
