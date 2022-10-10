from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_executor import Executor

cors = CORS(supports_credentials=True)
db = SQLAlchemy()
jwt = JWTManager()
executor = Executor()
