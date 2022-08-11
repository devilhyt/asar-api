import json
from pathlib import Path
from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from wingman_api.models.project import Project
from wingman_api.config import WINGMAN_ROOT

actions_root = Path(WINGMAN_ROOT, 'wingman_api', 'assets', 'actions')


class ActionAPI(MethodView):
    """Wingman Action API"""
    decorators = [jwt_required()]

    def get(self, project_name, action_name):
        """Get actions
        :param action_name:
            If action_name is None, then return all actions.\n
            Else, then return an action object.
        """
        # Receive
        mode = request.args.get('mode')
        # Implement
        prj = Project(project_name)
        if action_name:
            obj = prj.action.get(action_name)
            return jsonify(obj), 200
        elif mode == 'name':
            names = prj.action.names
            return jsonify(names), 200
        else:
            content = prj.action.content
            return jsonify(content), 200

    def post(self, project_name):
        """Create An action"""
        # Receive
        name = request.json.get('name')
        content = request.json.get('content', {})
        # Implement
        prj = Project(project_name)
        prj.action.create(name, content)
        return jsonify({"msg": "OK"}), 200

    def put(self, project_name, action_name):
        """Update A Intent"""
        # Receive
        new_name = request.json.get('new_name')
        content = request.json.get('content', {})
        # Implement
        prj = Project(project_name)
        prj.action.update(action_name, new_name, content)
        return jsonify({"msg": "OK"}), 200

    def delete(self, project_name, action_name):
        """Delete A Project"""
        # Implement
        prj = Project(project_name)
        prj.action.delete(action_name)
        return jsonify({"msg": "OK"}), 200


class ActionTypeAPI(MethodView):
    """Wingman Action Type API"""

    def get(self):
        """Get the names of all action types"""
        # Implement
        type_names = [d.stem for d in actions_root.iterdir() if d.is_dir()]
        return jsonify(type_names)


class ActionSchemaAPI(MethodView):
    """Wingman Action Schema API"""

    def get(self, type_name):
        """Get the schema of an action type"""
        type_names = [d.stem for d in actions_root.iterdir() if d.is_dir()]
        if type_name not in type_names:
            raise ValueError('Action type does not exist')

        schema_file = actions_root.joinpath(type_name, 'schema.json')

        # Implement
        with open(schema_file, 'r', encoding="utf-8") as json_file:
            schema_json = json.load(json_file)

        return jsonify(schema_json), 200


def init_app(app: Flask):
    action_view = ActionAPI.as_view('action_api')
    app.add_url_rule('/projects/<string:project_name>/actions',
                     defaults={'action_name': None},
                     view_func=action_view,
                     methods=['GET'])
    app.add_url_rule('/projects/<string:project_name>/actions',
                     view_func=action_view,
                     methods=['POST'])
    app.add_url_rule('/projects/<string:project_name>/actions/<string:action_name>',
                     view_func=action_view,
                     methods=['GET', 'PUT', 'DELETE'])
    action_type_view = ActionTypeAPI.as_view('action_type_api')
    app.add_url_rule('/actions/types',
                     view_func=action_type_view,
                     methods=['GET'])
    action_schema_view = ActionSchemaAPI.as_view('action_schema_api')
    app.add_url_rule('/actions/schema/<string:type_name>',
                     view_func=action_schema_view,
                     methods=['GET'])
