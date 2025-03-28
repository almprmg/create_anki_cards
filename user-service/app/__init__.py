import os
from flask import Flask
from .config import Config
from .database import init_db
from .auth import auth_blueprint
# from .routes import user_blueprint

def create_app():
    server = Flask(__name__)
    server.config.from_object(Config)
    
    init_db(server)
    server.config["POSTGERS_HOST"] = os.environ.get("POSTGERS_HOST")
    server.config["POSTGERS_USER"] = os.environ.get("POSTGERS_USER")
    server.config["POSTGERS_PASSWORD"] = os.environ.get("POSTGERS_PASSWORD")
    server.config["POSTGERS_DB"] = os.environ.get("POSTGERS_DB")
    server.config["POSTGERS_PORT"] = int(os.environ.get("POSTGERS_PORT"))

    server.register_blueprint(auth_blueprint, url_prefix='/auth')


    return server
