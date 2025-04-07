from flask_sqlalchemy import SQLAlchemy

db_session = SQLAlchemy()

def init_db(app):
    db_session.init_app(app)




    with app.app_context():
        db_session.create_all()  # This creates all tables defined in your models



