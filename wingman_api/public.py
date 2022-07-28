from flask import Flask
from flask_cors import CORS
from .config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
jwt = JWTManager(app)