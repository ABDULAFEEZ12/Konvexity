from flask_caching import Cache
from flask_compress import Compress
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)
compress = Compress()
cache = Cache()
cors = CORS()
talisman = Talisman()
login_manager = LoginManager()
