from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from ..models.project import Project
import shutil
from ..config import RASA_APP_ROOT, ACTIONS_PY_NAME

class ModelAPI(MethodView):
    """Asar Model API"""

    @jwt_required()
    def get(self, project_name):
        """Train a model"""
        # Implement
        prj = Project(project_name)
        prj.compile()
        
        status_code=200
        rasa_status_code=200
        msg = "test mode"
        # Todo: uncomment
        status_code, rasa_status_code, msg = prj.models.train()
        return jsonify({'rasa_status_code': rasa_status_code, 'msg': msg}), status_code                                     
        

    def post(self, project_name):
        """Callback"""
        # Implement
        prj = Project(project_name)
        if request.content_type == 'application/x-tar':
            prj.models.save(request.data)
        return jsonify({"msg": "OK"}), 200

    @jwt_required()
    async def put(self, project_name):
        """Load a model"""
        prj = Project(project_name)

        status_code=200
        rasa_status_code=200
        msg = "test mode"
        # Todo: uncomment
        status_code, rasa_status_code, msg = prj.models.load()
        shutil.copy(prj.actions.action_py_file, f'{RASA_APP_ROOT}/actions/{ACTIONS_PY_NAME}')
        return jsonify({'rasa_status_code': rasa_status_code, 'msg': msg}), status_code

    @classmethod
    def init_app(cls, app: Flask):
        model_view = cls.as_view('model_api')
        app.add_url_rule('/projects/<string:project_name>/models',
                         view_func=model_view,
                         methods=['GET', 'POST', 'PUT'])
