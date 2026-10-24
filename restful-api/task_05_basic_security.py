#!/usr/bin/python3
"""Implement HTTP Basic, JWT, and role-based Flask authentication."""
import os
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (
    JWTManager, create_access_token, get_jwt_identity, jwt_required
)
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY", "development-only-change-this-secret")
auth = HTTPBasicAuth()
jwt = JWTManager(app)
users = {
    "user1": {"username": "user1", "password": generate_password_hash(
        "password"), "role": "user"},
    "admin1": {"username": "admin1", "password": generate_password_hash(
        "password"), "role": "admin"}
}


@auth.verify_password
def verify_password(username, password):
    """Verify basic authentication credentials against stored hashes."""
    user = users.get(username)
    if user and check_password_hash(user["password"], password):
        return username
    return None


@jwt.unauthorized_loader
def missing_token(reason):
    """Return HTTP 401 for missing JWT credentials."""
    return jsonify({"error": "Missing or invalid token"}), 401


@jwt.invalid_token_loader
def invalid_token(reason):
    """Return HTTP 401 for invalid JWT credentials."""
    return jsonify({"error": "Invalid token"}), 401


@jwt.expired_token_loader
def expired_token(header, payload):
    """Return HTTP 401 for expired JWT credentials."""
    return jsonify({"error": "Token has expired"}), 401


@jwt.revoked_token_loader
def revoked_token(header, payload):
    """Return HTTP 401 for revoked JWT credentials."""
    return jsonify({"error": "Token has been revoked"}), 401


@jwt.needs_fresh_token_loader
def fresh_token(header, payload):
    """Return HTTP 401 when a fresh JWT token is required."""
    return jsonify({"error": "Fresh token required"}), 401


@app.route("/basic-protected")
@auth.login_required
def basic_protected():
    """Return a greeting for valid HTTP Basic credentials."""
    return "Basic Auth: Access Granted"


@app.route("/login", methods=["POST"])
def login():
    """Exchange valid credentials for a JWT access token."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid credentials"}), 401
    username = data.get("username")
    password = data.get("password")
    user = users.get(username) if isinstance(username, str) else None
    if not user or not isinstance(password, str) or not check_password_hash(
            user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401
    token = create_access_token(identity=username)
    return jsonify({"access_token": token})


@app.route("/jwt-protected")
@jwt_required()
def jwt_protected():
    """Return a greeting for a valid JWT access token."""
    return "JWT Auth: Access Granted"


@app.route("/admin-only")
@jwt_required()
def admin_only():
    """Grant access only to JWT users with the admin role."""
    user = users.get(get_jwt_identity())
    if not user or user.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403
    return "Admin Access: Granted"


if __name__ == "__main__":
    app.run()
