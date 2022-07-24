from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy

from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from flask.views import MethodView


app = Flask(__name__)


# Change this!
app.config["JWT_SECRET_KEY"] = "b0cf91e59567ee4951077964046cb574bddc5d9e461613d9c328f7089d448269"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


jwt = JWTManager(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

class AuthAPI(MethodView):
    @jwt_required()
    def get(self):
        '''get current user info'''
        return jsonify(id=current_user.id, username=current_user.username)

    def post(self):
        '''login'''
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        user = User.query.filter_by(username=username, password=password).one_or_none()
        if not user:
            return jsonify("Wrong username or password"), 401

        # Notice that we are passing in the actual sqlalchemy user object here
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token)

    # def delete(self, user_id):
    #     # delete a single user
    #     pass

    # def put(self, user_id):
    #     # update a single user
    #     pass


if __name__ == "__main__":
    # db.create_all()
    # db.session.add(User(username="admin", password="admin"))
    # db.session.add(User(username="user", password="user"))
    # db.session.commit()

    auth_view = AuthAPI.as_view('auth_api')
    app.add_url_rule('/auth', view_func=auth_view, methods=['GET', 'POST'])

    app.run(debug=True)
