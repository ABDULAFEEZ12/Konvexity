import os
from datetime import timedelta

from decouple import Csv, config


class BaseConfig:
    SECRET_KEY = config("SECRET_KEY", default="konvexity-development-secret-change-in-production")

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    DEBUG = False
    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 3600,
        "pool_pre_ping": True,
        "echo": False,
    }

    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600

    MAIL_SERVER = config("MAIL_SERVER", default="smtp.postmarkapp.com")
    MAIL_PORT = config("MAIL_PORT", default=587, cast=int)
    MAIL_USE_TLS = config("MAIL_USE_TLS", default=True, cast=bool)
    MAIL_USE_SSL = config("MAIL_USE_SSL", default=False, cast=bool)
    MAIL_USERNAME = config("MAIL_USERNAME", default="")
    MAIL_PASSWORD = config("MAIL_PASSWORD", default="")
    MAIL_DEFAULT_SENDER = config("MAIL_DEFAULT_SENDER", default="Konvexity <hello@konvexity.com>")
    MAIL_DEBUG = False

    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = config("RATELIMIT_STORAGE_URL", default="memory://")
    RATELIMIT_STRATEGY = "fixed-window"
    RATELIMIT_DEFAULT = "200 per day;50 per hour"

    CACHE_TYPE = config("CACHE_TYPE", default="SimpleCache")
    CACHE_DEFAULT_TIMEOUT = 300

    COMPRESS_MIN_SIZE = 500
    COMPRESS_LEVEL = 6
    COMPRESS_ALGORITHM = "gzip"

    BEHIND_PROXY = config("BEHIND_PROXY", default=False, cast=bool)

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = timedelta(days=30)


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = config(
        "DEV_DATABASE_URL",
        default="sqlite:///" + os.path.join(BaseConfig.BASE_DIR, "konvexity_dev.db")
    )
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False
    RATELIMIT_ENABLED = False
    COMPRESS_ENABLED = False


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = config("TEST_DATABASE_URL", default="sqlite:///:memory:")
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False
    COMPRESS_ENABLED = False
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = config(
        "DATABASE_URL",
        default="sqlite:///" + os.path.join(BaseConfig.BASE_DIR, "konvexity_prod.db")
    )
    SECRET_KEY = config("SECRET_KEY")
    MAIL_DEBUG = False
    RATELIMIT_ENABLED = True
    COMPRESS_ENABLED = True


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}