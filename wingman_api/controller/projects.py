from flask.views import MethodView
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required
from wingman_api.models.project import Project


class ProjectsAPI(MethodView):
    """Wingman Projects API"""

    @jwt_required()
    def get(self):
        """Retrieve All Project Names"""

        project_names = Project.names()
        return jsonify({"project_names": project_names})

    @jwt_required()
    def post(self):
        """Create A Project"""

        project_name = request.json.get("project_name", None)
        Project.create(project_name)
        return jsonify({"msg": "OK"}), 200

    @jwt_required()
    def put(self, project_name):
        """Update A Project"""

        new_project_name = request.json.get("new_project_name", None)
        prj = Project(project_name)
        prj.rename(new_project_name)
        return jsonify({"msg": "OK"}), 200

    @jwt_required()
    def delete(self, project_name):
        """Delete A Project"""

        prj = Project(project_name)
        prj.delete()
        return jsonify({"msg": "OK"}), 200


def init(app: Flask):
    projects_view = ProjectsAPI.as_view('projects_api')
    app.add_url_rule('/projects', view_func=projects_view,
                     methods=['GET', 'POST'])
    app.add_url_rule('/projects/<string:project_name>',
                     view_func=projects_view, methods=['PUT', 'DELETE'])
