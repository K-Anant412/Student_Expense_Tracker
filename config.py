import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def build_database_uri():
    """
    Constructs the database URI from environment variables.
    Supports either a full DATABASE_URL or component variables (DB_USER, DB_PASSWORD, etc.).
    """
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        if database_url.startswith("mysql://"):
            database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)
        return database_url

    db_user = os.getenv("DB_USER", "root")
    raw_password = os.getenv("DB_PASSWORD", "")
    db_password = quote_plus(raw_password) if raw_password else ""
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "student_expense_tracker")

    if db_password:
        return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
    else:
        return f"mysql+pymysql://{db_user}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"


class Config:
    """Base application configuration class."""
    SECRET_KEY = os.getenv("SECRET_KEY", "student-expense-tracker-secret-2026")
    SQLALCHEMY_DATABASE_URI = build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
        "pool_pre_ping": True,
    }
    FLASK_PORT = int(os.getenv("PORT", 5000))
    API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000/api")
    DEBUG = os.getenv("FLASK_ENV", "development").lower() == "development"


config = Config()
