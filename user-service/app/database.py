from flask_mysqldb import MySQL

db_session = MySQL()

def init_db(app):
    db_session.init_app(app)



