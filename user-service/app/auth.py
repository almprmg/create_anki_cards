from flask import Blueprint, request, jsonify

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from .models import User
from .utils import generate_token
from .database import db_session as db

auth_blueprint = Blueprint('auth', __name__)

SECRET_KEY = "your_secret_key"

@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    
    user = db_session.query(User).filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        token = generate_token(user)
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401





@auth_blueprint.route("/register", methods=["POST"])
def register():
    data = request.json
    role = data.get("role", "user")  # افتراضيًا المستخدم عادي
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
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity={"id": user.id, "role": user.role})
    return jsonify(access_token=access_token), 200


@auth_blueprint.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


