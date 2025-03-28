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
    server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
    server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
    server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
    server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
    server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))

    server.register_blueprint(auth_blueprint, url_prefix='/auth')


    return server
