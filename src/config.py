import os

class Config:
    """Database configuration for MySQL"""
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Vogen2025@localhost/itloginn"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True, 
        "pool_recycle": 3600, 
    }

# For development
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

# For testing
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

# For production
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
