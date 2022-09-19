from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from ..models.project import Project


class ProjectAPI(MethodView):
    """Asar Project API"""
    decorators = [jwt_required()]

    def get(self):
        """Get the names of all projects"""
        project_names = Project.names()
        return jsonify({"project_names": project_names})

    def post(self):
        """Create a project"""
        # Receive
        project_name = request.json.get('project_name')
        # Implement
        prj = Project(project_name)
        prj.create()
        return jsonify({"msg": "OK"}), 200

    def put(self, project_name):
        """Update A Project"""
        # Receive
        new_project_name = request.json.get('new_project_name')
        # Implement
        prj = Project(project_name)
        prj.rename(new_project_name)
        return jsonify({"msg": "OK"}), 200

    def delete(self, project_name):
        """Delete A Project"""
        # Implement
        prj = Project(project_name)
        prj.delete()
        return jsonify({"msg": "OK"}), 200

    @classmethod
    def init_app(cls, app: Flask):
        project_view = cls.as_view('project_api')
        app.add_url_rule('/projects', view_func=project_view,
                        methods=['GET', 'POST'])
        app.add_url_rule('/projects/<string:project_name>',
                        view_func=project_view,
                        methods=['PUT', 'DELETE'])