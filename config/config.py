import os

def build_sqlalchemy_database_uri():
    return f"mysql+mysqlconnector://{os.getenv('BAGHOLDER_MYSQL_USERNAME')}:{os.getenv('BAGHOLDER_MYSQL_PASSWORD')}@{os.getenv('BAGHOLDER_MYSQL_HOST')}:{os.getenv('BAGHOLDER_MYSQL_PORT')}/{os.getenv('BAGHOLDER_MYSQL_DATABASE')}"

class Config:
    SQLALCHEMY_DATABASE_URI = build_sqlalchemy_database_uri()
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", False)
    SECRET_KEY = os.getenv("BAGHOLDER_SECRET_KEY")
    MARKETDATA_ENDPOINT = os.getenv("MARKETDATA_ENDPOINT")
    MARKETDATA_API_TOKEN = os.getenv("MARKETDATA_API_TOKEN")
    BAGHOLDER_APPNAME = os.getenv("BAGHOLDER_APPNAME")
    AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
    MARKETSTACK_ENDPOINT = os.getenv("MARKETSTACK_ENDPOINT")
    MARKETSTACK_API_TOKEN = os.getenv("MARKETSTACK_API_TOKEN")


class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = True