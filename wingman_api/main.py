from flask import Flask
from .config import DevelopmentConfig
from .extensions import cors, db, jwt
import wingman_api.config
import wingman_api.public
import wingman_api.controller.auth
import wingman_api.controller.project
import wingman_api.controller.intent
import wingman_api.controller.action
import wingman_api.controller.story
import wingman_api.controller.rule
import wingman_api.controller.token
import wingman_api.controller.tokenizer


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
    wingman_api.controller.intent.init_app(app)
    wingman_api.controller.action.init_app(app)
    wingman_api.controller.story.init_app(app)
    wingman_api.controller.rule.init_app(app)
    wingman_api.controller.token.init_app(app)
    wingman_api.controller.tokenizer.init_app(app)
    return app
