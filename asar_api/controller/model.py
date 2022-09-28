from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from ..models.project import Project
import os

class ModelAPI(MethodView):
    """Asar Model API"""

    @jwt_required()
    def get(self, project_name):
        """Train a model"""
        # Implement
        prj = Project(project_name)
        prj.compile()
        rasa_api_url = os.getenv("RASA_API_URL")
        asar_api_url = os.getenv("ASAR_API_URL")
        
        if rasa_api_url and asar_api_url:
            status_code=200
            # Todo: uncomment
            # status_code = prj.models.train(rasa_api_url=rasa_api_url,asar_api_url=asar_api_url)
            return jsonify({'rasa_status_code': status_code}), 200
        else:
            return jsonify({'msg': 'RASA_API_URL or ASAR_API_URL environment variable not found'}), 400                                       
        

    def post(self, project_name):
        """Callback"""
        # Implement
        prj = Project(project_name)
        if request.content_type == 'application/x-tar':
            prj.models.save(request.data)
        return jsonify({"msg": "OK"}), 200

    @jwt_required()
    async def put(self, project_name):
        prj = Project(project_name)
        rasa_api_url = os.getenv("RASA_API_URL")
        if rasa_api_url:
            status_code = prj.models.load(rasa_api_url=rasa_api_url)
            return jsonify({'rasa_status_code': status_code}), 200
        else:
            return jsonify({'msg': 'RASA_API_URL environment variable not found'}), 400

    @classmethod
    def init_app(cls, app: Flask):
        model_view = cls.as_view('model_api')
        app.add_url_rule('/projects/<string:project_name>/models',
                         view_func=model_view,
                         methods=['GET', 'POST', 'PUT'])
