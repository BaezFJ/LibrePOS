import os

from dotenv import load_dotenv

load_dotenv()

# Application Settings
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

TIMEZONE = os.getenv("TIMEZONE", "America/New_York")
CURRENCY = os.getenv("CURRENCY", "USD")
DATE_FORMAT = os.getenv("DATE_FORMAT", "%m/%d/%Y")
TIME_FORMAT = os.getenv("TIME_FORMAT", "%I:%M %p")
LANGUAGE = os.getenv("LANGUAGE", "en")
BABEL_DEFAULT_LOCALE = os.getenv("BABEL_DEFAULT_LOCALE", "en_US")


# Flask Settings
def _to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


DEBUG = _to_bool(os.getenv("DEBUG"), False)
TESTING = _to_bool(os.getenv("TESTING"), False)

# Ensure SECRET_KEY is always set; in production prefer env var
_secret_from_env = os.getenv("SECRET_KEY")
if _secret_from_env:
    SECRET_KEY = _secret_from_env
elif DEBUG or TESTING:
    SECRET_KEY = "development-and-testing-key-not-for-production"
else:
    raise RuntimeError(
        "Production SECRET_KEY must be configured via environment variable. (.env) "
        "Set the SECRET_KEY environment variable with a secure value."
    )

# Flask-SQLAlchemy Settings
SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "librepos.db")
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Mailman
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_USE_TLS = _to_bool(os.getenv("MAIL_USE_TLS"), False)
MAIL_USE_SSL = _to_bool(os.getenv("MAIL_USE_SSL"), False)
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
MAIL_SUPPRESS_SEND = _to_bool(os.getenv("MAIL_SUPPRESS_SEND"), False)
