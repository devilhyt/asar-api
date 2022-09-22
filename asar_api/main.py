from flask import Flask
from .config import DevelopmentConfig
from .extensions import cors, db, jwt
import asar_api.public
from .controller.auth import AuthAPI
from .controller.project import ProjectAPI
from .controller.tokenizer import TokenizerAPI
from .controller.model import ModelAPI
from .controller.api_basis import ApiBasis
from .controller.gconfig import GConfigAPI
from .controller.lconfig import LConfigAPI


def create_app(config=DevelopmentConfig):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config)
    config.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    
    asar_api.public.init_app(app)
    AuthAPI.init_app(app)
    GConfigAPI.init_app(app)
    ProjectAPI.init_app(app)
    LConfigAPI.init_app(app)
    ApiBasis.init_app(app, 'intents', 'path')
    ApiBasis.init_app(app, 'actions', 'path')
    ApiBasis.init_app(app, 'entities')
    ApiBasis.init_app(app, 'slots')
    ApiBasis.init_app(app, 'stories')
    ApiBasis.init_app(app, 'rules')
    ApiBasis.init_app(app, 'tokens')
    TokenizerAPI.init_app(app)
    ModelAPI.init_app(app)
    return app
