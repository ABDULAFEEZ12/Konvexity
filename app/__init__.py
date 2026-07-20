# app/__init__.py

import logging
import os
import signal
import sys
import time

import click
from flask import Flask, g, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix

logger = logging.getLogger("konvexity")


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "production")

    app = Flask(
        "konvexity",
        template_folder="templates",
        static_folder="static",
        static_url_path="/static",
    )

    from app.config import config_by_name
    app.config.from_object(config_by_name[config_name])

    configure_extensions(app)
    configure_blueprints(app)
    configure_error_handlers(app)
    configure_request_hooks(app)
    configure_context_processors(app)
    configure_security_headers(app)
    configure_proxy_support(app)
    configure_shutdown_handler(app)
    configure_cli_commands(app)

    if not app.config.get("TESTING"):
        configure_production_logging(app)

    logger.info(
        "Konvexity application created [config=%s, debug=%s, testing=%s]",
        config_name,
        app.config["DEBUG"],
        app.config.get("TESTING", False),
    )

    return app


def configure_extensions(app):
    from app.extensions import cache, compress, cors, db, limiter, mail, migrate

    db.init_app(app)
    migrate.init_app(app, db, directory=os.path.join(app.root_path, "..", "migrations"))
    mail.init_app(app)

    if not app.config.get("TESTING"):
        limiter.init_app(app)

    compress.init_app(app)
    cache.init_app(app)
    cors.init_app(app)


def configure_blueprints(app):
    from app.blueprints.public.routes import public_bp
    app.register_blueprint(public_bp)


def configure_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.exception("Internal server error: %s", str(error))
        return render_template("errors/500.html"), 500


def configure_request_hooks(app):
    @app.before_request
    def before_request():
        g.request_start_time = time.time()

    @app.after_request
    def after_request(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(), interest-cohort=()"
        return response


def configure_context_processors(app):
    import datetime as dt

    @app.context_processor
    def inject_globals():
        return {
            "site_name": "Konvexity",
            "site_tagline": "Where Clarity Meets Growth",
            "current_year": dt.datetime.now().year,
        }

    @app.context_processor
    def inject_navigation():
        navigation = {
            "primary": [
                {"label": "Home", "url": "/"},
                {"label": "About", "url": "/about"},
                {"label": "Solutions", "url": "/solutions"},
                {"label": "Programs", "url": "/programs"},
                {"label": "Faculty", "url": "/faculty"},
                {"label": "Founder", "url": "/founder"},
                {"label": "Clients", "url": "/clients"},
                {"label": "Contact", "url": "/contact"},
            ]
        }
        return {"navigation": navigation}


def configure_security_headers(app):
    if not app.config.get("DEBUG"):
        from app.extensions import talisman
        talisman.init_app(
            app,
            content_security_policy={
                "default-src": "'self'",
                "script-src": ["'self'", "'unsafe-inline'", "https://cdn.tailwindcss.com"],
                "style-src": ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
                "font-src": ["'self'", "https://fonts.gstatic.com"],
                "img-src": ["'self'", "data:", "https:"],
                "connect-src": ["'self'"],
                "frame-src": ["'none'"],
                "object-src": ["'none'"],
                "base-uri": ["'self'"],
                "form-action": ["'self'"],
            },
            content_security_policy_nonce_in=["script-src"],
        )


def configure_proxy_support(app):
    if app.config.get("BEHIND_PROXY", False):
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


def configure_shutdown_handler(app):
    def graceful_shutdown(signum, frame):
        logger.info("Received shutdown signal %s. Cleaning up...", signum)
        from app.extensions import db
        try:
            db.session.remove()
            db.engine.dispose()
            logger.info("Database connections closed.")
        except Exception as exc:
            logger.error("Error during shutdown cleanup: %s", exc)
        sys.exit(0)

    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)


def configure_cli_commands(app):
    @app.cli.command("init-db")
    def init_db():
        from app.extensions import db
        db.create_all()
        click.echo("Database tables created.")


def configure_production_logging(app):
    from logging.handlers import RotatingFileHandler

    log_dir = os.path.join(app.root_path, "..", "logs")
    os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "konvexity.log"),
        maxBytes=10_485_760,
        backupCount=10,
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Konvexity production logging configured.")