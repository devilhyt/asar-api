from flask import Flask
from .config import DevelopmentConfig
from .extensions import cors, db, jwt
import wingman_api.config
import wingman_api.public
from wingman_api.controller.auth import AuthAPI
from wingman_api.controller.project import ProjectAPI
from wingman_api.controller.tokenizer import TokenizerAPI
from wingman_api.controller.action_ext import ActionExt
from wingman_api.controller.model import ModelAPI
from wingman_api.controller.api_basis import ApiBasis


def create_app(config=DevelopmentConfig):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config)
    wingman_api.config.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    wingman_api.public.init_app(app)
    AuthAPI.init_app(app)
    ProjectAPI.init_app(app)
    ApiBasis.init_app(app, 'intents', 'path')
    ApiBasis.init_app(app, 'actions', 'path')
    ApiBasis.init_app(app, 'entities')
    ApiBasis.init_app(app, 'slots')
    ApiBasis.init_app(app, 'stories')
    ApiBasis.init_app(app, 'rules')
    ApiBasis.init_app(app, 'tokens')
    TokenizerAPI.init_app(app)
    ActionExt.init_app(app)
    ModelAPI.init_app(app)
    return app
