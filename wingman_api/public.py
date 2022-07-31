from flask import Flask, jsonify
from flask_cors import CORS
from .config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
jwt = JWTManager(app)

@app.errorhandler(Exception)
def handle_exception(e : Exception):
    print(e)
    return jsonify({"msg":str(e)}), 400