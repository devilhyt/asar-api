from flask import Flask, jsonify
from flask_cors import CORS
from .config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

import wingman_api.controller.project
import wingman_api.controller.intent
import wingman_api.controller.action
import wingman_api.controller.story

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
jwt = JWTManager(app)

import wingman_api.controller.auth
wingman_api.controller.auth.init(app)
wingman_api.controller.project.init(app)
wingman_api.controller.intent.init(app)
wingman_api.controller.action.init(app)
wingman_api.controller.story.init(app)

@app.errorhandler(Exception)
def handle_exception(e : Exception):
    app.logger.error(e)
    return jsonify({"msg":str(e)}), 400