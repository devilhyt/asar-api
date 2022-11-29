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
        status_code, msgCode, msg = prj.create()
        return jsonify({'msgCode': msgCode, 'msg': msg}), status_code

    def put(self, project_name):
        """Update A Project"""
        # Receive
        new_name = request.json.get('new_name')
        # Implement
        prj = Project(project_name)
        status_code, msgCode, msg = prj.rename(new_name)
        return jsonify({'msgCode': msgCode, 'msg': msg}), status_code

    def delete(self, project_name):
        """Delete A Project"""
        # Implement
        prj = Project(project_name)
        # TODO: delete this
        # if project_name in ['居家管家', '餐飲服務機器人', '個人助理']:
        #     raise ValueError('展示用專案，禁止刪除！')
        status_code, msgCode, msg = prj.delete()
        return jsonify({'msgCode': msgCode, 'msg': msg}), status_code

    @classmethod
    def init_app(cls, app: Flask):
        project_view = cls.as_view('project_api')
        app.add_url_rule('/projects', view_func=project_view,
                         methods=['GET', 'POST'])
        app.add_url_rule('/projects/<string:project_name>',
                         view_func=project_view,
                         methods=['PUT', 'DELETE'])
