import os


def build_sqlalchemy_database_uri():
    username = os.getenv("BAGHOLDER_MYSQL_USERNAME", "alone")
    password = os.getenv("BAGHOLDER_MYSQL_PASSWORD")
    host = os.getenv("BAGHOLDER_MYSQL_HOST", "localhost")
    port = os.getenv("BAGHOLDER_MYSQL_PORT", "3306")
    database = os.getenv("BAGHOLDER_MYSQL_DATABASE", "bagholdercuy")
    return f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8mb4"


class Config:
    SQLALCHEMY_DATABASE_URI = build_sqlalchemy_database_uri()
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", False)
    SECRET_KEY = os.getenv("BAGHOLDER_SECRET_KEY", "default-bagholder-secret-key-12345")
    MARKETDATA_ENDPOINT = os.getenv("MARKETDATA_ENDPOINT")
    MARKETDATA_API_TOKEN = os.getenv("MARKETDATA_API_TOKEN")
    BAGHOLDER_APPNAME = os.getenv("BAGHOLDER_APPNAME", "bagholdercuy")
    AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "default-auth-secret-key-12345")
    MARKETSTACK_ENDPOINT = os.getenv("MARKETSTACK_ENDPOINT")
    MARKETSTACK_API_TOKEN = os.getenv("MARKETSTACK_API_TOKEN")
    ALPHAVANTAGE_KEY = os.getenv("ALPHAVANTAGE_KEY")
    MASSIVE_ENDPOINT = os.getenv("MASSIVE_ENDPOINT", "https://api.massive.com")
    MASSIVE_API_TOKEN = os.getenv("MASSIVE_API_TOKEN")
    FILE_STORAGE_PATH = os.getenv(
        "FILE_STORAGE_PATH", "/home/alone/data/bagholderdata/"
    )
    INTERACTIVE_BROKERS_ENDPOINT = os.getenv("INTERACTIVE_BROKERS_ENDPOINT")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = True
