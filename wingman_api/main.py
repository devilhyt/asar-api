from flask import Flask
from .config import DevelopmentConfig
from .extensions import cors, db, jwt
import wingman_api.config
import wingman_api.public
import wingman_api.controller.auth
import wingman_api.controller.project
import wingman_api.controller.tokenizer
import wingman_api.controller.action_ext
import wingman_api.controller.rasa_model
from wingman_api.controller.api_basis import ApiBasis


def create_app(config=DevelopmentConfig):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config)
    wingman_api.config.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    wingman_api.public.init_app(app)
    wingman_api.controller.auth.init_app(app)
    wingman_api.controller.project.init_app(app)
    ApiBasis.init_app(app, 'intents', 'path')
    ApiBasis.init_app(app, 'actions', 'path')
    ApiBasis.init_app(app, 'entities')
    ApiBasis.init_app(app, 'slots')
    ApiBasis.init_app(app, 'stories')
    ApiBasis.init_app(app, 'rules')
    ApiBasis.init_app(app, 'tokens')
    wingman_api.controller.tokenizer.init_app(app)
    wingman_api.controller.action_ext.init_app(app)
    wingman_api.controller.rasa_model.init_app(app)
    return app
