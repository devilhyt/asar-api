from flask.views import MethodView
from flask import Flask, jsonify, request
from flask_jwt_extended import current_user, jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt, get_jwt_identity
from wingman_api.public import jwt, app
from wingman_api.models.user import User

from datetime import datetime, timedelta, timezone


class AuthAPI(MethodView):
    @jwt_required()
    def get(self):
        """get current user info"""
        return jsonify(id=current_user.id, username=current_user.username)

    def post(self):
        """get current user info"""
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        user = User.query.filter_by(
            username=username, password=password).one_or_none()
        if not user:
            return jsonify("Wrong username or password"), 400

        # Notice that we are passing in the actual sqlalchemy user object here
        access_token = create_access_token(identity=user.id)
        response = jsonify(access_token=access_token)
        set_access_cookies(response, access_token)
        return response

    @jwt_required()
    def delete(self):
        """get current user info"""
        response = jsonify({"msg": "logout successful"})
        unset_jwt_cookies(response)
        return response


def init(app: Flask):
    auth_view = AuthAPI.as_view('auth_api')
    app.add_url_rule('/auth', view_func=auth_view,
                     methods=['GET', 'POST', 'DELETE'])

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
        Register a callback function that loads a user from your database whenever a protected route is accessed. 
        This should return any python object on a successful lookup, or None if the lookup failed for any reason (for example if the user has been deleted from the database).
    """
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@app.after_request
def refresh_expiring_jwts(response):
    """
        Using an `after_request` callback, we refresh any token that is within 30 minutes of expiring. 
        Change the timedeltas to match the needs of your application.
    """
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response

# @jwt.user_identity_loader
# def user_identity_lookup(user):
#     """
#         Register a callback function that takes whatever object is passed in as the identity when creating JWTs and converts it to a JSON serializable format
#     """
#     return user.id