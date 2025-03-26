from flask import Flask
from .config import Config
from .database import init_db
from .auth import auth_blueprint
from .routes import user_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    init_db(app)

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprint, url_prefix='/users')

    return app
