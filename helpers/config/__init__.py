import os

class Config(object):
    TESTING = False

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    # .env variable
    USER_DB = os.getenv("USER_DB")
    PASSWORD_DB = os.getenv("PASSWORD_DB")
    DB_NAME = os.getenv("DB_NAME")
    URI_DB = os.getenv("URI_DB")
    PORT_DB = os.getenv("PORT_DB")
    MY_SECRET = os.getenv("MY_SECRET")
    DB_URL = f"postgresql://{USER_DB}:{PASSWORD_DB}@{URI_DB}:{PORT_DB}/{DB_NAME}"

    # Configuration
    SECRET_KEY = "Your_secret_string"
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

def get_config():
    config_name = os.getenv("FLASK_ENV")

    config_by_name = dict(
        development=DevelopmentConfig,
        test=TestingConfig,
        production=ProductionConfig
    )

    return config_by_name[config_name]