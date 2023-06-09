#!/usr/bin/env python3
'''
File: app.py
'''
from flask import Flask, jsonify

app: Flask = Flask(__name__)

@app.route("/")
def welcome() -> str:
    return jsonify({"message": "Bienvenue"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

