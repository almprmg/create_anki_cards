# app/__init__.py
from flask import Flask
from app.config import app_config
from app.infrastructure.database import db_session, shutdown_session, init_db


def create_app(config_name=None):
    """App Factory Pattern"""
    app = Flask(__name__)


    app.config.from_object(app_config)


    @app.cli.command('init-db')
    def init_db_command():
        """Clear existing data and create new tables."""
        init_db()
        print('Initialized the database.')

    # Register a function to close the database session after each request
    @app.teardown_appcontext
    def teardown_db(exception=None):
        shutdown_session(exception)

    # --- تسجيل الـ Blueprints ---
    from .api.decks import decks_bp 
    app.register_blueprint(decks_bp, url_prefix='/api/v1') 

  # (We'll record other Blueprints here later, like cards_bp)

# --- Other settings (like CORS, Logging) will added here ---

    print(f" * Flask App created with config: {app.config['ENV']}")
    return app