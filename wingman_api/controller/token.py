from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from wingman_api.models.project import Project


class TokenAPI(MethodView):
    """Wingman Token API"""
    decorators = [jwt_required()]

    def get(self, project_name, token_name):
        """
        :param token_name:
            If token_name is None, then get the names of all tokens.\n
            If token_name is not None, then get an token object.
        """
        # Receive
        mode = request.args.get('mode')
        # Implement
        prj = Project(project_name)
        if token_name:
            token_obj = prj.token.get(token_name)
            return jsonify(token_obj), 200
        elif mode == 'name':
            token_names = prj.token.names
            return jsonify(token_names), 200
        else:
            tokens = prj.token.content
            return jsonify(tokens), 200

    def post(self, project_name):
        """Create a token"""
        # Receive
        content = request.json
        token_name = content.pop('token_name', None)
        # Implement
        prj = Project(project_name)
        prj.token.create(token_name, content)
        return jsonify({"msg": "OK"}), 200

    def put(self, project_name, token_name):
        """Update a token"""
        # Receive
        content = request.json
        new_token_name = content.pop('new_token_name', None)
        # Implement
        prj = Project(project_name)
        prj.token.update(token_name, new_token_name, content)
        return jsonify({"msg": "OK"}), 200

    def delete(self, project_name, token_name):
        """Delete a token"""
        # Implement
        prj = Project(project_name)
        prj.token.delete(token_name)
        return jsonify({"msg": "OK"}), 200


def init_app(app: Flask):

    token_view = TokenAPI.as_view('token_api')
    app.add_url_rule('/projects/<string:project_name>/tokens',
                     defaults={'token_name': None},
                     view_func=token_view,
                     methods=['GET'])
    app.add_url_rule('/projects/<string:project_name>/tokens',
                     view_func=token_view,
                     methods=['POST'])
    app.add_url_rule('/projects/<string:project_name>/tokens/<string:token_name>',
                     view_func=token_view,
                     methods=['GET', 'PUT', 'DELETE'])
