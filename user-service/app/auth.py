from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from .models import User
from .utils import generate_token
from .database import db_session

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

def generate_token(user):
    payload = {
        "username": user.username,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
