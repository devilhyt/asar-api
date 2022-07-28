from flask.views import MethodView
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required
from wingman_api.utils.project import Project
from wingman_api.config import WINGMAN_ROOT
from pathlib import Path
import json

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

        prj = Project(project_name)
        if action_name:
            action_obj = prj.action.content[action_name]
            return jsonify(action_obj), 200
        else:
            action_names = prj.action.names
            return jsonify({'action_name': action_names}), 200

    @jwt_required()
    def post(self, project_name):
        """Create An action"""

        prj = Project(project_name)
        content = request.json
        action_name = content.pop('action_name', None)
        prj.action.create(action_name, content)
        return jsonify({"msg": "OK"}), 200

    @jwt_required()
    def put(self, project_name, action_name):
        """Update A Intent"""

        prj = Project(project_name)
        content = request.json
        new_action_name = content.pop('new_action_name', None)
        prj.action.update(action_name, new_action_name, content)
        return jsonify({"msg": "OK"}), 200

    @jwt_required()
    def delete(self, project_name, action_name):
        """Delete A Project"""

        prj = Project(project_name)
        prj.action.delete(action_name)
        return jsonify({"msg": "OK"}), 200


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

        type_names = [d.stem for d in actions_root.iterdir() if d.is_dir()]
        if type_name not in type_names:
            raise ValueError('Action type does not exist')

        schema_file = actions_root.joinpath(type_name, 'schema.json')

        # Implement
        with open(schema_file, 'r', encoding="utf-8") as json_file:
            schema_json = json.load(json_file)

        return jsonify(schema_json), 200


def init(app: Flask):

    actions_view = ActionsAPI.as_view('actions_api')
    app.add_url_rule('/projects/<string:project_name>/actions',
                     defaults={'action_name': None},
                     view_func=actions_view,
                     methods=['GET'])
    app.add_url_rule('/projects/<string:project_name>/actions',
                     view_func=actions_view,
                     methods=['POST'])
    app.add_url_rule('/projects/<string:project_name>/actions/<string:action_name>',
                     view_func=actions_view,
                     methods=['GET', 'PUT', 'DELETE'])

    action_type_view = ActionTypeAPI.as_view('action_type_api')
    app.add_url_rule('/actions/types',
                     view_func=action_type_view,
                     methods=['GET'])

    action_schema_view = ActionSchemaAPI.as_view('action_schema_api')
    app.add_url_rule('/actions/schema/<string:type_name>',
                     view_func=action_schema_view,
                     methods=['GET'])
