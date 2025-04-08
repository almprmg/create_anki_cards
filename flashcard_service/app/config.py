import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'DefaultSecretKeyIfNotSet') #
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    REDIS_AI_REQUEST_CHANNEL = os.environ.get('REDIS_AI_REQUEST_CHANNEL', 'ai_generation_requests')
    REDIS_AI_RESULT_CHANNEL = os.environ.get('REDIS_AI_RESULT_CHANNEL', 'ai_generation_results')
    

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    FLASK_ENV = 'development'
    # يمكنك استخدام قاعدة بيانات SQLite للتطوير السريع إذا أردت
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class ProductionConfig(Config):
    """Production configuration."""
    FLASK_ENV = 'production'


env = os.environ.get('FLASK_ENV', 'development')
if env == 'production':
    app_config = ProductionConfig()
else:
    app_config = DevelopmentConfig()
