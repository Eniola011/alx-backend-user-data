#!/usr/bin/env python3
"""

Flask App

"""


from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def karibu() -> str:
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
        return jsonify({"email": user.email, "message":
                        "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
        >> Function  responds to the POST /sessions route.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    is_valid_login = auth.valid_login(email, password)

    if is_valid_login:
        session_id = auth.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
       >> Function responds to the DELETE /sessions route.
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = auth.get_user_from_session_id(session_id)
    if user:
        auth.destroy_session(user_id)
        return redirect('/')
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
