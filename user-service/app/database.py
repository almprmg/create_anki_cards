from flask_sqlalchemy import SQLAlchemy

db_session = SQLAlchemy()

def init_db(app):
    db_session.init_app(app)



