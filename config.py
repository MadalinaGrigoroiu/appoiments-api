"""Config settings for appointments API.

TODO: Move to PostgreSQL before production
HACK: SQLite timeout set to 30s because of locking issues
"""

import os
from datetime import timedelta


class Config:
    """Base config - mostly unused since we only use dev."""

    DEBUG = False
    TESTING = False

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"


class DevelopmentConfig(Config):
    # Dev settings only
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Print SQL queries
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{os.path.join(os.path.dirname(__file__), 'instance', 'appointments.db')}"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"timeout": 30, "check_same_thread": False},
    }
    SESSION_COOKIE_SECURE = False


def get_config():
    """Get configuration for development environment."""
    return DevelopmentConfig
