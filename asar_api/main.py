from pathlib import Path
from flask import Flask
from .extensions import cors, db, jwt, executor
from .config import DevelopmentConfig, ASAR_DATA_ROOT
import asar_api.public
from .routes.auth import AuthAPI
from .routes.project import ProjectAPI
from .routes.model import ModelAPI, ModelCallbackAPI
from .routes.api_basis import ApiBasis
from .routes.lconfig import LConfigAPI


def create_app(config=DevelopmentConfig):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config)
    config.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    executor.init_app(app)

    # database
    with app.app_context():
        from .models.user import User
        from .models.server_status import ServerStatus
        Path(ASAR_DATA_ROOT).mkdir(parents=True, exist_ok=True)
        db.create_all()
        User.init()
        ServerStatus.init()

    asar_api.public.init_app(app)
    AuthAPI.init_app(app)
    ProjectAPI.init_app(app)
    LConfigAPI.init_app(app)
    ApiBasis.init_app(app, 'intents', 'path')
    ApiBasis.init_app(app, 'responses', 'path')
    ApiBasis.init_app(app, 'actions', 'path')
    ApiBasis.init_app(app, 'entities')
    ApiBasis.init_app(app, 'slots')
    ApiBasis.init_app(app, 'stories')
    ApiBasis.init_app(app, 'rules')
    ApiBasis.init_app(app, 'synonyms')
    ApiBasis.init_app(app, 'forms')
    ModelAPI.init_app(app)
    ModelCallbackAPI.init_app(app)
    return app
