from flask import Flask, jsonify
from flask_cors import CORS
from .config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


cors = CORS(supports_credentials=True)
db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    cors.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    
    import wingman_api.controller.auth
    import wingman_api.controller.project
    import wingman_api.controller.intent
    import wingman_api.controller.action
    import wingman_api.controller.story
    wingman_api.controller.auth.init(app)
    wingman_api.controller.project.init(app)
    wingman_api.controller.intent.init(app)
    wingman_api.controller.action.init(app)
    wingman_api.controller.story.init(app)

    @app.errorhandler(Exception)
    def handle_exception(e: Exception):
        app.logger.error(e)
        return jsonify({"msg": str(e)}), 400

    # test page
    @app.get("/")
    def hello_world_get():
        return "<p>Hello, World!</p>"

    from flask import request

    @app.post("/<string:test_string>")
    def hello_world_post(test_string):
        app.logger.info(request.view_args)
        app.logger.info(request.json)
        return "<p>Hello, World!</p>"

    return app
