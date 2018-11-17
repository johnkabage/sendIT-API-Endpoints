import os

class Config:
    DEBUG = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    DATABASE_URL = os.getenv("DATABASE_URL")

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


app_config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}