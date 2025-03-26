import jwt
from datetime import datetime, timedelta
from .config import Config
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

def generate_token(user):
    payload = {
        "username": user.username,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user.get("role") != "admin":
            return jsonify({"message": "Access forbidden"}), 403
        return f(*args, **kwargs)
    return wrapper