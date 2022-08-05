from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

cors = CORS(app, supports_credentials=True)
db = SQLAlchemy(app)
jwt = JWTManager(app)

# cors.init_app(app)
# db.init_app(app)
# jwt.init_app(app)

@app.errorhandler(Exception)
def handle_exception(e: Exception):
    app.logger.error(e)
    return jsonify({"msg": str(e)}), 400