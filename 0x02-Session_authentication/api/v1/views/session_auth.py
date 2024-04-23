g!/usr/bin/env python3
"""

Session Authentication Routes Handler

"""


from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User
from api.v1.auth.session_auth import SessionAuth
from api.v1.app import auth


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
        >> User Login with Session authentication.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
