#!/usr/bin/env python3.8
'''
File: app.py
'''
from flask import Flask, jsonify, request, make_response, abort
from auth import Auth

app: Flask = Flask(__name__)
AUTH = Auth()


@app.route("/")
def welcome() -> str:
    """return a JSON payload of the form"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user() -> str:
    """endpoint to register a user"""
    email: str = request.form.get("email")
    password: str = request.form.get("password")

    try:
        user: User = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({'email': email, 'message': 'logged in'})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """
    Logout route to destroy the session for the user with the given session ID
    """
    session_id: str = request.cookies.get("session_id")
    user: Optional[User] = auth.get_user_from_session_id(session_id)
    if user:
        auth.destroy_session(user.id)
        return "Logged out successfully"
    else:
        abort(403)


@app.route("/profile", methods=["GET"])
def profile() -> str:
    """
    Profile route to retrieve user profile based on session ID
    """
    session_id: str = request.cookies.get("session_id")
    user = auth.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """
    Get reset password token"""
    email: str = request.form.get('email')

    try:
        reset_token: str = auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    '''update password'''
    email: str = request.form.get('email')
    reset_token: str = request.form.get('reset_token')
    new_password: str = request.form.get('new_password')

    try:
        auth.update_password(reset_token, new_password)
        return jsonify({'email': email, 'message': 'Password updated'}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
