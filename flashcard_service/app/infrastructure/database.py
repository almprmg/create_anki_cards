
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.config import app_config
from app.models.base import Base 

engine = create_engine(app_config.SQLALCHEMY_DATABASE_URI)


session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Create a scoped session to ensure that each request gets its own session.
# This is very useful in web applications to avoid concurrency issues.
db_session = scoped_session(session_factory)

def init_db():
    """Creates all tables defined in models."""
 
    from app.models import deck, card
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

def shutdown_session(exception=None):
    """Removes the current session when the request ends."""
    db_session.remove()

# Note: You'll need to bind shutdown_session to the teardown_appcontext event in Flask later.