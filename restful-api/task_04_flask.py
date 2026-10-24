#!/usr/bin/python3
"""Provide a small Flask API for in-memory user records."""
from flask import Flask, jsonify, request


app = Flask(__name__)
users = {}


@app.route("/")
def home():
    """Return the home greeting."""
    return "Welcome to the Flask API!"


@app.route("/data")
def data():
    """Return a list of usernames."""
    return jsonify(list(users.keys()))


@app.route("/status")
def status():
    """Return a simple health status."""
    return "OK"


@app.route("/users/<username>")
def get_user(username):
    """Return a user or a not-found error."""
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify(users[username])


@app.route("/add_user", methods=["POST"])
def add_user():
    """Validate and add a new user to memory."""
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return jsonify({"error": "Invalid JSON"}), 400
    username = body.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400
    if username in users:
        return jsonify({"error": "Username already exists"}), 409
    users[username] = body
    return jsonify({"message": "User added", "user": body}), 201


if __name__ == "__main__":
    app.run()
