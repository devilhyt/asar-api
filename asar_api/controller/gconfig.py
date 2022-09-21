from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from ..models.gconfig import GConfig

class GConfigAPI(MethodView):
    """Asar GConfig API"""
    decorators = [jwt_required()]

    def get(self):
        """Get global config"""

        # Implement
        cfg = GConfig()
        return jsonify(cfg.content), 200
    
    def put(self):
        """Update global config"""
        # Receive
        content = request.json
        # Implement
        cfg = GConfig()
        cfg.update(content)
        return jsonify({"msg": "OK"}), 200

    @classmethod
    def init_app(cls, app: Flask):
        cfg = GConfig()
        cfg.init()
        view = cls.as_view(f'gconfig_api')
        app.add_url_rule(f'/gconfig',
                         view_func=view,
                         methods=['GET', 'PUT'])