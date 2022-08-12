from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from wingman_api.models.project import Project


class ApiBasis(MethodView):
    """Wingman API"""
    decorators = [jwt_required()]

    def __init__(self, api_name: str) -> None:
        self.api_name = api_name

    def get(self, project_name, name):
        """Get objects
        :param name:
            If name is None, then return all objects.\n
            Else, then return an object.
        """
        # Receive
        mode = request.args.get('mode')
        # Implement
        prj = Project(project_name)
        objs = getattr(prj, self.api_name)
        if name:
            obj = objs.get(name)
            return jsonify(obj), 200
        elif mode == 'name':
            names = objs.names
            return jsonify(names), 200
        else:
            content = objs.content
            return jsonify(content), 200

    def post(self, project_name):
        """Create an object"""
        # Receive
        name = request.json.get('name')
        content = request.json.get('content', {})
        # Implement
        prj = Project(project_name)
        objs = getattr(prj, self.api_name)
        objs.create(name, content)
        return jsonify({"msg": "OK"}), 200

    def put(self, project_name, name):
        """Update an object"""
        # Receive
        new_name = request.json.get('new_name')
        content = request.json.get('content', {})
        # Implement
        prj = Project(project_name)
        objs = getattr(prj, self.api_name)
        objs.update(name, new_name, content)
        return jsonify({"msg": "OK"}), 200

    def delete(self, project_name, name):
        """Delete an object"""
        # Implement
        prj = Project(project_name)
        objs = getattr(prj, self.api_name)
        objs.delete(name)
        return jsonify({"msg": "OK"}), 200


def init_app(app: Flask, api_name: str, name_type: str = 'string'):
    view = ApiBasis.as_view(f'{api_name}_api', api_name)
    app.add_url_rule(f'/projects/<string:project_name>/{api_name}',
                     defaults={'name': None},
                     view_func=view,
                     methods=['GET'])
    app.add_url_rule(f'/projects/<string:project_name>/{api_name}',
                     view_func=view,
                     methods=['POST'])
    app.add_url_rule(f'/projects/<string:project_name>/{api_name}/<{name_type}:name>',
                     view_func=view,
                     methods=['GET', 'PUT', 'DELETE'])
