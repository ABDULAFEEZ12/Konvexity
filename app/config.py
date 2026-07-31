import os
from datetime import timedelta

from decouple import Csv, config


class BaseConfig:
    SECRET_KEY = config("SECRET_KEY", default="konvexity-development-secret-change-in-production")

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    DEBUG = False
    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # pool_size/pool_recycle are QueuePool (Postgres) options that SQLite's
    # pool implementation rejects outright. Previously set unconditionally
    # here, which meant DevelopmentConfig/TestingConfig (both default to
    # SQLite) crashed on db.init_app() the moment DEV_DATABASE_URL/
    # TEST_DATABASE_URL weren't overridden to Postgres. Kept minimal and
    # SQLite-safe here; the Postgres-specific pool tuning now lives on
    # ProductionConfig, where SQLALCHEMY_DATABASE_URI is actually Postgres.
    SQLALCHEMY_ENGINE_OPTIONS = {
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
    # No site-wide RATELIMIT_DEFAULT: rate limiting is applied per-route,
    # only on sensitive actions (admin login, public form submissions),
    # via explicit @limiter.limit(...) decorators. A blanket default here
    # previously rate-limited ordinary page browsing itself, since every
    # page load pulls in several requests (HTML, CSS, JS, images), a
    # handful of real page views could exhaust a low daily limit for a
    # legitimate visitor within minutes.

    CACHE_TYPE = config("CACHE_TYPE", default="SimpleCache")
    CACHE_DEFAULT_TIMEOUT = 300

    COMPRESS_MIN_SIZE = 500
    COMPRESS_LEVEL = 6
    COMPRESS_ALGORITHM = "gzip"

    BEHIND_PROXY = config("BEHIND_PROXY", default=False, cast=bool)

    # NOTE: previously "BASE_DIR/app/static/uploads", which does not exist.
    # app/__init__.py serves static files from PROJECT_ROOT/static (BASE_DIR
    # here IS PROJECT_ROOT), so uploads must live under BASE_DIR/static to be
    # reachable at the URLs Flask actually serves. Fixed as part of the CRM
    # file-upload foundation, since the old path silently produced
    # unreachable files.
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_UPLOAD_EXTENSIONS = {"pdf", "doc", "docx", "png", "jpg", "jpeg", "webp"}

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
    # Postgres (psycopg2) supports QueuePool tuning; SQLite's pool
    # implementation raises TypeError on pool_size/pool_recycle rather than
    # ignoring them, which is exactly the bug this split fixes. If
    # DATABASE_URL is ever pointed at SQLite in production, remove these
    # two keys or the app will fail to start, same as it did before this
    # fix for Development/Testing.
    SQLALCHEMY_ENGINE_OPTIONS = {
        **BaseConfig.SQLALCHEMY_ENGINE_OPTIONS,
        "pool_size": 10,
        "pool_recycle": 3600,
    }
    SECRET_KEY = config("SECRET_KEY")
    MAIL_DEBUG = False
    RATELIMIT_ENABLED = True
    COMPRESS_ENABLED = True


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
