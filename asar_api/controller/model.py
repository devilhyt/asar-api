from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from ..models.project import Project
import shutil
from ..config import RASA_APP_ROOT, ACTIONS_PY_NAME
from ..models.server_status import ServerStatus
from ..extensions import db, executor


class ModelAPI(MethodView):
    """Asar Model API"""
    decorators = [jwt_required()]

    def get(self):
        """Get training info"""
        server_status = ServerStatus.query.first()
        return jsonify({'training_status': server_status.training_status,
                        'training_result': server_status.training_result,
                        'training_message': server_status.training_message,
                        'training_project': server_status.training_project,
                        'loaded_status': server_status.loaded_status,
                        'loaded_result': server_status.loaded_result,
                        'loaded_message': server_status.loaded_message,
                        'loaded_project': server_status.loaded_project}), 200

    def post(self):
        """Train a model"""
        debug = False
        # Receive
        project_name = request.json.get('project_name')
        # Implement
        prj = Project(project_name)
        prj.compile()
        status_code, msg = prj.models.train(debug=debug)
        return jsonify({'msg': msg}), status_code

    def put(self):
        """Load a model"""
        debug = False
        # Receive
        project_name = request.json.get('project_name')
        # Implement
        prj = Project(project_name)
        status_code, msg = prj.models.load_checker(debug=debug)
        
        if status_code == 200:
            executor.submit(self.load_bg, project_name, debug)
            
        return jsonify({'msg': msg}), status_code
    
    def load_bg(self, project_name:str, debug:bool):
        prj = Project(project_name)
        result = prj.models.load_bg(debug=debug)
        if result and not debug:
            shutil.copy(prj.actions.action_py_file,
                        f'{RASA_APP_ROOT}/actions/{ACTIONS_PY_NAME}')

    @classmethod
    def init_app(cls, app: Flask):
        model_view = cls.as_view('model_api')
        app.add_url_rule('/models',
                         view_func=model_view,
                         methods=['GET', 'POST', 'PUT'])


class ModelCallbackAPI(MethodView):
    """Asar Model Callback API"""

    def post(self, project_name):
        """Callback"""
        # Implement
        prj = Project(project_name)
        server_status = ServerStatus.query.first()
        server_status.training_status = False

        if request.content_type == 'application/x-tar':
            prj.models.save(request.data)
            server_status.training_result = 1
            server_status.training_message = 'ok'

        elif request.content_type == 'application/json':
            server_status.training_result = 0
            server_status.training_message = request.json.get(
                'status') + request.json.get('message')

        db.session.commit()

        return jsonify({"msg": "OK"}), 200

    @classmethod
    def init_app(cls, app: Flask):
        model_callback_view = cls.as_view('model_callback_api')
        app.add_url_rule('/projects/<string:project_name>/models',
                         view_func=model_callback_view,
                         methods=['POST'])
