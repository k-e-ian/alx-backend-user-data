#!/usr/bin/env python3
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
