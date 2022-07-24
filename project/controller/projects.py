from flask.views import MethodView
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required
from project.config import WINGMAN_PRJ_DIR, WINGMAN_PRJ_SUB_DIR
from pathlib import Path
import shutil

project_dir = Path(WINGMAN_PRJ_DIR)

project_dir.mkdir(parents=True, exist_ok=True)


class ProjectsAPI(MethodView):
    """Wingman Projects API"""
    
    @jwt_required()
    def get(self):
        """Retrieve All Project Names"""

        subdirs = [d.stem for d in project_dir.iterdir() if d.is_dir()]
        return jsonify(projectName=subdirs)

    @jwt_required()
    def post(self):
        """Create A New Project"""

        try:
            projectName = request.json.get("projectName", None)
            
            ProjectsAPI.check_name(projectName)  
            
            for sub in WINGMAN_PRJ_SUB_DIR:
                project_dir.joinpath(f'{projectName}/{sub}').mkdir(parents=True)
        except Exception as e:
            response = jsonify({"msg": str(e), "projectName": projectName})
            return response, 400
        else:
            response = jsonify({"msg": "OK", "projectName": projectName})
            return response, 200

    @jwt_required()
    def put(self, projectName):
        """Update A Project"""
                
        try:
            newProjectName = request.json.get("newProjectName", None)
            
            ProjectsAPI.check_name(projectName)
            ProjectsAPI.check_name(newProjectName)
            
            target = project_dir.joinpath(newProjectName)
            project_dir.joinpath(projectName).rename(target)
        except Exception as e:
            response = jsonify({"msg": str(e), "projectName": projectName, "newProjectName": newProjectName})
            return response, 400
        else:
            response = jsonify({"msg": "OK", "projectName": projectName, "newProjectName": newProjectName})
            return response, 200

    @jwt_required()
    def delete(self, projectName):
        """Delete A Project"""

        try:
            ProjectsAPI.check_name(projectName)
            p = project_dir.joinpath(projectName)
            shutil.rmtree(p)
        except Exception as e:
            response = jsonify({"msg": str(e), "projectName": projectName})
            return response, 400
        else:
            response = jsonify({"msg": "OK", "projectName": projectName})
            return response, 200
                
    @staticmethod
    def check_name(name: str):
        """avoid relative path"""
        
        if ".." in name:
            raise ValueError('Invalid project name')

def init(app: Flask):
    projects_view = ProjectsAPI.as_view('projects_api')
    app.add_url_rule('/projects', view_func=projects_view,
                     methods=['GET', 'POST'])
    app.add_url_rule('/projects/<string:projectName>',
                     view_func=projects_view, methods=['PUT', 'DELETE'])
