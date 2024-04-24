#!/usr/bin/env python3
"""

Session Authentication Routes Handler

"""


from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
        >> User Login with Session authentication.
    """
    usr_email = request.form.get('email')
    if not usr_email:
        return jsonify({"error": "email missing"}), 400
    usr_password = request.form.get('password')
    if not usr_password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': usr_email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    for usr in user:
        if usr.is_valid_password(usr_password):
            from api.v1.app import auth
            session_id = auth.create_session(usr.id)
            response = jsonify(usr.to_json())
            response.set_cookie(getenv('SESSION_NAME'), session_id)
            return response
        else:
            return jsonify({"error": "wrong password"}), 401


@app_views.route('/api/v1/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """
       >> User Logout with Session authentication.
    """
    from api.v1.app import auth
    kill_session = auth.destroy_session(request)
    if kill_session is False:
        abort(404)
    else:
        return jsonify({}), 200
