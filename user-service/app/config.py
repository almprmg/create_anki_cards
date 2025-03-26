class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost:5432/user_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'
