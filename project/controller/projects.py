from flask.views import MethodView
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required
from project.config import WINGMAN_PRJ_DIR, WINGMAN_PRJ_SUB
from pathlib import Path
import shutil
from project import util

prj_root = Path(f'{WINGMAN_PRJ_DIR}')

class ProjectsAPI(MethodView):
    """Wingman Projects API"""
    
    @jwt_required()
    def get(self):
        """Retrieve All Project Names"""

        prj_names = [d.stem for d in prj_root.iterdir() if d.is_dir()]
        return jsonify(projectName=prj_names)

    @jwt_required()
    def post(self):
        """Create A Project"""

        try:
            projectName = request.json.get("projectName", None)
            
            util.check_name(projectName)
            
            prj_dir = prj_root.joinpath(f'{projectName}')
            prj_dir.mkdir(parents=True)
            
            for dir, files in WINGMAN_PRJ_SUB.items():
                sub_dir = prj_dir.joinpath(f'{dir}')
                sub_dir.mkdir(parents=True)
                for f in files:
                    sub_file = sub_dir.joinpath(f'{f}')
                    sub_file.touch()
                    if sub_file.suffix == '.json':
                        sub_file.write_text('{}')
            
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
            
            util.check_name(projectName)
            util.check_name(newProjectName)
            
            target = prj_root.joinpath(newProjectName)
            prj_root.joinpath(projectName).rename(target)
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
            util.check_name(projectName)
            p = prj_root.joinpath(projectName)
            shutil.rmtree(p)
        except Exception as e:
            response = jsonify({"msg": str(e), "projectName": projectName})
            return response, 400
        else:
            response = jsonify({"msg": "OK", "projectName": projectName})
            return response, 200

def init(app: Flask):
    prj_root.mkdir(parents=True, exist_ok=True)
    
    projects_view = ProjectsAPI.as_view('projects_api')
    app.add_url_rule('/projects', view_func=projects_view,
                     methods=['GET', 'POST'])
    app.add_url_rule('/projects/<string:projectName>',
                     view_func=projects_view, methods=['PUT', 'DELETE'])
