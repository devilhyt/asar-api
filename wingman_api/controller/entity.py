from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from wingman_api.models.project import Project


class EntityAPI(MethodView):
    """Wingman Entity API"""
    decorators = [jwt_required()]

    def get(self, project_name, entity_name):
        """Get entities
        :param entity_name:
            If entity_name is None, then return all entities.\n
            Else, then return an entity object.
        """
        # Receive
        mode = request.args.get('mode')
        # Implement
        prj = Project(project_name)
        if entity_name:
            obj = prj.entities.get(entity_name)
            return jsonify(obj), 200
        elif mode == 'name':
            names = prj.entities.names
            return jsonify(names), 200
        else:
            content = prj.entities.content
            return jsonify(content), 200

    def post(self, project_name):
        """Create an entity"""
        # Receive
        name = request.json.get('name')
        content = request.json.get('content', {})
        # Implement
        prj = Project(project_name)
        prj.entities.create(name, content)
        return jsonify({"msg": "OK"}), 200

    def put(self, project_name, entity_name):
        """Update an entity"""
        # Receive
        new_name = request.json.get('new_name')
        content = request.json.get('content', {})
        # Implement
        prj = Project(project_name)
        prj.entities.update(entity_name, new_name, content)
        return jsonify({"msg": "OK"}), 200

    def delete(self, project_name, entity_name):
        """Delete an entity"""
        # Implement
        prj = Project(project_name)
        prj.entities.delete(entity_name)
        return jsonify({"msg": "OK"}), 200


def init_app(app: Flask):
    entity_view = EntityAPI.as_view('entity_api')
    app.add_url_rule('/projects/<string:project_name>/entities',
                     defaults={'entity_name': None},
                     view_func=entity_view,
                     methods=['GET'])
    app.add_url_rule('/projects/<string:project_name>/entities',
                     view_func=entity_view,
                     methods=['POST'])
    app.add_url_rule('/projects/<string:project_name>/entities/<string:entity_name>',
                     view_func=entity_view,
                     methods=['GET', 'PUT', 'DELETE'])
