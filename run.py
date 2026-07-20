import os
import sys

from decouple import config as env_config
from dotenv import load_dotenv

load_dotenv()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
if APP_ROOT not in sys.path:
    sys.path.insert(0, APP_ROOT)


def main():
    from app import create_app

    config_name = env_config("FLASK_CONFIG", default="development")
    debug_mode = env_config("FLASK_DEBUG", default="1") == "1"

    application = create_app(config_name=config_name)

    host = env_config("FLASK_HOST", default="127.0.0.1")
    port = env_config("FLASK_PORT", default=5000, cast=int)

    if config_name == "production":
        print("")
        print("=" * 72)
        print("  WARNING: Running production config with development server.")
        print("  This is not safe for live deployments.")
        print("  Use: gunicorn wsgi:app --bind 0.0.0.0:8000 --workers 4")
        print("=" * 72)
        print("")

    application.run(
        host=host,
        port=port,
        debug=debug_mode,
        use_reloader=debug_mode,
        use_debugger=debug_mode,
        load_dotenv=False,
    )


if __name__ == "__main__":
    main()