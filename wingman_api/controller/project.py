from flask.views import MethodView
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required
from wingman_api.models.project import Project, ProjectSchema, ProjectSchemaUpdate


class ProjectAPI(MethodView):
    """Wingman Project API"""

    @jwt_required()
    def get(self):
        """Retrieve All Project Names"""

        project_names = Project.names()
        return jsonify({"project_names": project_names})

    @jwt_required()
    def post(self):
        """Create A Project"""

        # Receive
        project_name = request.json.get("project_name", None)
        # Validation
        valid_data = ProjectSchema(project_name=project_name)
        # Implement
        Project.create(valid_data.project_name)
        return jsonify({"msg": "OK"}), 200

    @jwt_required()
    def put(self, project_name):
        """Update A Project"""

        # Receive
        new_project_name = request.json.get("new_project_name", None)
        # Validation
        valid_data = ProjectSchemaUpdate(project_name=project_name, new_project_name=new_project_name)
        # Implement
        prj = Project(valid_data.project_name)
        prj.rename(valid_data.new_project_name)
        return jsonify({"msg": "OK"}), 200

    @jwt_required()
    def delete(self, project_name):
        """Delete A Project"""

        # Validation
        valid_data = ProjectSchema(project_name=project_name)
        # Implement
        prj = Project(valid_data.project_name)
        prj.delete()
        return jsonify({"msg": "OK"}), 200


def init(app: Flask):
    project_view = ProjectAPI.as_view('project_api')
    app.add_url_rule('/projects', view_func=project_view,
                     methods=['GET', 'POST'])
    app.add_url_rule('/projects/<string:project_name>',
                     view_func=project_view, 
                     methods=['PUT', 'DELETE'])
