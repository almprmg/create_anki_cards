import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'DefaultSecretKeyIfNotSet') #
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # تعطيل تتبع تعديلات SQLAlchemy لتحسين الأداء
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # المفتاح المستخدم لفك تشفير JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

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
