from flask.views import MethodView
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required
from wingman_api.utils.project import Project


class IntentsAPI(MethodView):
    """Wingman Intents API"""

    @jwt_required()
    def get(self, project_name, intent_name):
        """
        :param intent_name:
            If intent_name is None, then Retrieve All Intent Names.\n
            If intent_name is not None, then Get An intent.
        """

        prj = Project(project_name)
        if intent_name:
            intent_obj = prj.intent.content[intent_name]
            return jsonify(intent_obj), 200
        else:
            intent_names = prj.intent.names
            return jsonify({'intent_names': intent_names}), 200

    @jwt_required()
    def post(self, project_name):
        """Create An intent"""

        prj = Project(project_name)
        intent_name = request.json.get('intent_name', None)
        prj.intent.create(intent_name)
        return jsonify({"msg": "OK"}), 200

    @jwt_required()
    def put(self, project_name, intent_name):
        """Update An Intent"""

        prj = Project(project_name)
        content = request.json
        new_intent_name = content.pop('new_intent_name', None)
        prj.intent.update(intent_name, new_intent_name, content)
        return jsonify({"msg": "OK"}), 200

    @jwt_required()
    def delete(self, project_name, intent_name):
        """Delete An Intent"""

        prj = Project(project_name)
        prj.intent.delete(intent_name)
        return jsonify({"msg": "OK"}), 200


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
