#!/usr/bin/env python3
'''
File: app.py
'''
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
