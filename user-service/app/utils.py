
from .config import Config
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity , create_access_token
from flask import jsonify

import os
import redis



redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0
)



def create_response(message, status_code, data=None):
    response = {"message": message}
    if data:
        response["data"] = data
    return jsonify(response), status_code
def generate_token(user):
    payload = {
        "username": user.username,
        "role": user.role,
       
    }
    return create_access_token(identity=payload)   



def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user.get("role") != "admin":
            return jsonify({"message": "Access forbidden"}), 403
        return f(*args, **kwargs)
    return wrapper


def store_token(username, token):
    key = f"auth_token:{username}"
    redis_client.setex(key, Config. TOKEN_EXPIRY, token)

def check_login_attempts(username):
    key = f"login_attempts:{username}"
    attempts = redis_client.get(key)
    if attempts and int(attempts) >= Config.MAX_ATTEMPTS:
        return False
    return True

def record_failed_attempt(username):
    key = f"login_attempts:{username}"
    attempts = redis_client.incr(key)
    if attempts == 1:
        redis_client.expire(key, Config.LOCKOUT_TIME)


# def verify_token(token):
#     decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
#     username = decoded["username"]
#     key = f"auth_token:{username}"
#     stored_token = redis_client.get(key)
#     if stored_token and stored_token.decode() == token:
#         return decoded
#     return None