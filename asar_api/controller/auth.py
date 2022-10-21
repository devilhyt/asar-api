from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import (current_user,
                                jwt_required,
                                create_access_token,
                                set_access_cookies,
                                unset_jwt_cookies, get_jwt,
                                get_jwt_identity)
from ..models.user import User, UserSchema, UserChangePasswordSchema
from ..extensions import db, jwt


class AuthAPI(MethodView):
    """Asar Auth API"""
    @jwt_required()
    def get(self):
        """get current user info"""
        return jsonify(id=current_user.id, username=current_user.username)

    def post(self):
        """login"""
        # Receive
        content = request.json
        # Validation
        valid_data = UserSchema.parse_obj(content)
        # Implement
        user: User = User.query.filter_by(
            username=valid_data.username).one_or_none()

        if not user.check_password(valid_data.password):
            return jsonify({'msgCode': 'loginFailed', 'msg': 'Wrong username or password.'}), 400

        access_token = create_access_token(identity=user.id)
        response = jsonify({'access_token': access_token,
                           'msgCode': 'success', 'msg': 'Logged in.'})
        set_access_cookies(response, access_token)
        return response, 200

    @jwt_required()
    def put(self):
        """change password"""
        # Receive
        content = request.json
        # Validation
        valid_data = UserChangePasswordSchema.parse_obj(content)
        # Implement
        user: User = User.query.filter_by(
            username=current_user.username).one_or_none()

        if not user.check_password(valid_data.password):
            return jsonify({'msgCode': 'wrongPassword', 'msg': 'Wrong password.'}), 400

        user.set_password(valid_data.new_password)
        db.session.commit()

        # access_token = create_access_token(identity=user.id)
        # response = jsonify(access_token=access_token)
        # set_access_cookies(response, access_token)
        response = jsonify(
            {'msgCode': 'success', 'msg': 'Your password has been successfully changed.'})
        return response, 200

    @jwt_required()
    def delete(self):
        """logout"""
        response = jsonify({'msgCode': 'success', 'msg': 'Logged out.'})
        unset_jwt_cookies(response)
        return response, 200

    @classmethod
    def init_app(cls, app: Flask):

        auth_view = cls.as_view('auth_api')
        app.add_url_rule('/auth',
                         view_func=auth_view,
                         methods=['GET', 'POST', 'PUT', 'DELETE'])
        app.after_request(refresh_expiring_jwts)


def refresh_expiring_jwts(response):
    """
        Using an `after_request` callback, we refresh any token that is within 30 minutes of expiring. 
        Change the timedeltas to match the needs of your application.
    """
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(hours=1))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
        Register a callback function that loads a user from your database whenever a protected route is accessed. 
        This should return any python object on a successful lookup, or None if the lookup failed for any reason (for example if the user has been deleted from the database).
    """
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()
