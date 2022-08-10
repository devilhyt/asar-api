from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from wingman_api.models.project import Project


class IntentAPI(MethodView):
    """Wingman Intent API"""
    decorators = [jwt_required()]

    def get(self, project_name, intent_name):
        """
        :param intent_name:
            If intent_name is None, then get the names of all intents.\n
            If intent_name is not None, then get an intent object.
        """
        # Receive
        mode = request.args.get('mode')
        # Implement
        prj = Project(project_name)
        if intent_name:
            intent_obj = prj.intent.get(intent_name)
            return jsonify(intent_obj), 200
        elif mode == 'name':
            intent_names = prj.intent.names
            return jsonify(intent_names), 200
        else:
            intents = prj.intent.content
            return jsonify(intents), 200

    def post(self, project_name):
        """Create An intent"""
        # Receive
        intent_name = request.json.get('intent_name')
        # Implement
        prj = Project(project_name)
        prj.intent.create(intent_name)
        return jsonify({"msg": "OK"}), 200

    def put(self, project_name, intent_name):
        """Update An Intent"""
        # Receive
        content = request.json
        new_intent_name = content.pop('new_intent_name', None)
        # Implement
        prj = Project(project_name)
        prj.intent.update(intent_name, new_intent_name, content)
        return jsonify({"msg": "OK"}), 200

    def delete(self, project_name, intent_name):
        """Delete An Intent"""
        # Implement
        prj = Project(project_name)
        prj.intent.delete(intent_name)
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
    app.add_url_rule('/projects/<string:project_name>/intents/<string:intent_name>',
                     view_func=intent_view,
                     methods=['GET', 'PUT', 'DELETE'])
