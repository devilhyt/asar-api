from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from wingman_api.models.project import Project


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
            obj = prj.actions.get(action_name)
            return jsonify(obj), 200
        elif mode == 'name':
            names = prj.actions.names
            return jsonify(names), 200
        else:
            content = prj.actions.content
            return jsonify(content), 200

    def post(self, project_name):
        """Create an action"""
        # Receive
        name = request.json.get('name')
        content = request.json.get('content', {})
        # Implement
        prj = Project(project_name)
        prj.actions.create(name, content)
        return jsonify({"msg": "OK"}), 200

    def put(self, project_name, action_name):
        """Update an action"""
        # Receive
        new_name = request.json.get('new_name')
        content = request.json.get('content', {})
        # Implement
        prj = Project(project_name)
        prj.actions.update(action_name, new_name, content)
        return jsonify({"msg": "OK"}), 200

    def delete(self, project_name, action_name):
        """Delete an action"""
        # Implement
        prj = Project(project_name)
        prj.actions.delete(action_name)
        return jsonify({"msg": "OK"}), 200


def init_app(app: Flask):
    action_view = ActionAPI.as_view('action_api')
    app.add_url_rule('/projects/<string:project_name>/actions',
                     defaults={'action_name': None},
                     view_func=action_view,
                     methods=['GET'])
    app.add_url_rule('/projects/<string:project_name>/actions',
                     view_func=action_view,
                     methods=['POST'])
    app.add_url_rule('/projects/<string:project_name>/actions/<path:action_name>',
                     view_func=action_view,
                     methods=['GET', 'PUT', 'DELETE'])
