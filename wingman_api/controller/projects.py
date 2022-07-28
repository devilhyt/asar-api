from flask.views import MethodView
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required
from wingman_api.config import WINGMAN_PRJ_DIR, WINGMAN_PRJ_STRUCT
from pathlib import Path
import shutil
from wingman_api import util

prj_root = Path(WINGMAN_PRJ_DIR)

class ProjectsAPI(MethodView):
    """Wingman Projects API"""
    
    @jwt_required()
    def get(self):
        """Retrieve All Project Names"""

        # Implement
        prj_names = [d.stem for d in prj_root.iterdir() if d.is_dir()]
        return jsonify(project_name=prj_names)

    @jwt_required()
    def post(self):
        """Create A Project"""

        try:
            project_name = request.json.get("project_name", None)
            
            # Validity check
            util.check_name(project_name)
            
            # Implement
            prj_dir = prj_root.joinpath(f'{project_name}')
            prj_dir.mkdir(parents=True)
            
            for dir, files in WINGMAN_PRJ_STRUCT.items():
                sub_dir = prj_dir.joinpath(f'{dir}')
                sub_dir.mkdir(parents=True)
                for f in files:
                    sub_file = sub_dir.joinpath(f'{f}')
                    sub_file.touch()
                    if sub_file.suffix == '.json':
                        sub_file.write_text('{}')
            
        except Exception as e:
            response = jsonify({"msg": str(e)})
            return response, 400
        else:
            response = jsonify({"msg": "OK"})
            return response, 200

    @jwt_required()
    def put(self, project_name):
        """Update A Project"""
                
        try:
            new_project_name = request.json.get("new_project_name", None)
            
            # Validity check
            util.check_name(project_name)
            util.check_name(new_project_name)
            
            # Implement
            target = prj_root.joinpath(new_project_name)
            prj_root.joinpath(project_name).rename(target)
        except Exception as e:
            response = jsonify({"msg": str(e)})
            return response, 400
        else:
            response = jsonify({"msg": "OK"})
            return response, 200

    @jwt_required()
    def delete(self, project_name):
        """Delete A Project"""

        try:
            # Validity check
            util.check_name(project_name)
            
            # Implement
            p = prj_root.joinpath(project_name)
            shutil.rmtree(p)
        except Exception as e:
            response = jsonify({"msg": str(e)})
            return response, 400
        else:
            response = jsonify({"msg": "OK"})
            return response, 200

def init(app: Flask):
    prj_root.mkdir(parents=True, exist_ok=True)
    
    projects_view = ProjectsAPI.as_view('projects_api')
    app.add_url_rule('/projects', view_func=projects_view,
                     methods=['GET', 'POST'])
    app.add_url_rule('/projects/<string:project_name>',
                     view_func=projects_view, methods=['PUT', 'DELETE'])
