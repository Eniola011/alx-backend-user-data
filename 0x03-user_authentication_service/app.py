#!/usr/bin/env python3
"""

Flask App

"""


from flask import Flask, jsonify, request
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
        return jsonify({"email": "<registered email>", "message":
                        "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
