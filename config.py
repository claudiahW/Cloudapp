import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class TestConfig(Config):
    pass
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    pass
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://claudbae:12345@localhost/claudapp2'
    DEBUG = True
config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'test': TestConfig
}