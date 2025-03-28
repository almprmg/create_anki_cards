import jwt, os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User
from .utils import generate_token , record_failed_attempt
from .utils import check_login_attempts ,admin_required , redis_client
from .database import db_session as db

auth_blueprint = Blueprint('auth', __name__)






@auth_blueprint.route("/register", methods=["POST"])
def register():
    data = request.json
    role = data.get("role", "user")  
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "User already exists"}), 400

    new_user = User(
        username=data["username"],
        email=data["email"],
        role=role
    )
    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.commit()


    

    return jsonify({"message": "User registered successfully"}), 201

@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    if not check_login_attempts(username):
        return jsonify({"message": "Too many failed attempts. Try again later."}), 403

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        record_failed_attempt(username)
        return jsonify({"message": "Invalid credentials"}), 401

    token = generate_token(user)
    return jsonify({"token": token}), 200


@auth_blueprint.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except:
        return "not authorized", 403

    return decoded, 200



@auth_blueprint.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    key = f"auth_token:{current_user['username']}"
    redis_client.delete(key)
    return jsonify({"message": "Logged out successfully"}), 200
@auth_blueprint.route("/protected", methods=["GET"])


@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@auth_blueprint.route("/admin/users", methods=["GET"])
@admin_required
def get_all_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "role": user.role} for user in users])