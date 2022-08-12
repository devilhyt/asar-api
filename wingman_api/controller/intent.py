from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from wingman_api.models.project import Project


class IntentAPI(MethodView):
    """Wingman Intent API"""
    decorators = [jwt_required()]

    def get(self, project_name, intent_name):
        """Get intents
        :param intent_name:
            If intent_name is None, then return all intents.\n
            Else, then return an intent object.
        """
        # Receive
        mode = request.args.get('mode')
        # Implement
        prj = Project(project_name)
        if intent_name:
            obj = prj.intents.get(intent_name)
            return jsonify(obj), 200
        elif mode == 'name':
            names = prj.intents.names
            return jsonify(names), 200
        else:
            content = prj.intents.content
            return jsonify(content), 200

    def post(self, project_name):
        """Create an intent"""
        # Receive
        name = request.json.get('name')
        content = request.json.get('content', {})
        # Implement
        prj = Project(project_name)
        prj.intents.create(name, content)
        return jsonify({"msg": "OK"}), 200

    def put(self, project_name, intent_name):
        """Update an intent"""
        # Receive
        new_name = request.json.get('new_name')
        content = request.json.get('content', {})
        # Implement
        prj = Project(project_name)
        prj.intents.update(intent_name, new_name, content)
        return jsonify({"msg": "OK"}), 200

    def delete(self, project_name, intent_name):
        """Delete an intent"""
        # Implement
        prj = Project(project_name)
        prj.intents.delete(intent_name)
        return jsonify({"msg": "OK"}), 200


def init_app(app: Flask):
    intent_view = IntentAPI.as_view('intent_api')
    app.add_url_rule('/projects/<string:project_name>/intents',
                     defaults={'intent_name': None},
                     view_func=intent_view,
                     methods=['GET'])
    app.add_url_rule('/projects/<string:project_name>/intents',
                     view_func=intent_view,
                     methods=['POST'])
    app.add_url_rule('/projects/<string:project_name>/intents/<path:intent_name>',
                     view_func=intent_view,
                     methods=['GET', 'PUT', 'DELETE'])
