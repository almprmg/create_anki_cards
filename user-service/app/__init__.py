import os

from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_migrate import Migrate
from .config import Config
from .database import init_db ,db_session
from .auth import auth_blueprint

# from .routes import user_blueprint

server = Flask(__name__)
server.config.from_object(Config)
server.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET")
server.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
server.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)
jwt = JWTManager(server)
server.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/postgres"#osenviron.get("DB_URL")



init_db(server)
migrate = Migrate(server, db_session)


server.register_blueprint(auth_blueprint, url_prefix='/auth')


