import logging
import os
import sys

from decouple import config as env_config
from dotenv import load_dotenv

load_dotenv(override=False)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
if APP_ROOT not in sys.path:
    sys.path.insert(0, APP_ROOT)

LOG_LEVEL = env_config("LOG_LEVEL", default="INFO").upper()
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
    stream=sys.stdout,
)

logger = logging.getLogger("konvexity")
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

from app import create_app

config_name = env_config("FLASK_CONFIG", default="production")

logger.info("Bootstrapping Konvexity application with config: %s", config_name)

application = create_app(config_name=config_name)

logger.info("Konvexity application initialized successfully.")