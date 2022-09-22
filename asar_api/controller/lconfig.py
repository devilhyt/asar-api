from flask import Flask, jsonify, request, make_response
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from ..models.project import Project

class LConfigAPI(MethodView):
    """Asar LConfig API"""
    decorators = [jwt_required()]

    def get(self, project_name):
        """Get local config"""

        # Implement
        prj = Project(project_name)
        r = make_response(prj.lconfigs.content)
        r.mimetype = 'text/x-yaml'
        return r
    
    def put(self, project_name):
        """Update local config"""
        # Receive
        content = request.data.decode('utf-8')
        # Implement
        prj = Project(project_name)
        prj.lconfigs.update(content)
        return jsonify({"msg": "OK"}), 200

    @classmethod
    def init_app(cls, app: Flask):
        view = cls.as_view(f'lconfig_api')
        app.add_url_rule(f'/projects/<string:project_name>/lconfigs',
                         view_func=view,
                         methods=['GET', 'PUT'])