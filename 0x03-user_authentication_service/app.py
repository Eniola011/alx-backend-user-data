#!/usr/bin/env python3
"""

Flask App

"""


from flask import Flask, jsonify, request, make_response, abort
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """
       >> Welcome Message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """
       >> Function implements the POST /users route.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = auth.register_user(email, password)
        return jsonify({"email": email, "message":
                        "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
        >> Function  responds to the POST /sessions route.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(400)
    if auth.valid_login(email, password):
        session_id = auth.create_session(email)
        if session_id:
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie('session_id', session_id)
            return response, 200
    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
