import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ----------------------------
# Defaults and constants
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_TIMEZONE = "America/New_York"
DEFAULT_CURRENCY = "USD"
DEFAULT_DATE_FORMAT = "%m/%d/%Y"
DEFAULT_TIME_FORMAT = "%I:%M %p"
DEFAULT_LANGUAGE = "en"
DEFAULT_BABEL_LOCALE = "en_US"
DEFAULT_SQLITE_FILENAME = "librepos.db"
DEFAULT_DEV_SECRET = "development-and-testing-key-not-for-production"

# Truthy tokens for _to_bool parsing
_TRUTHY_TOKENS = {"1", "true", "yes", "on"}


# ----------------------------
# Helpers
# ----------------------------
def _to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in _TRUTHY_TOKENS


def _env_str(name: str, default: str | None = None) -> str | None:
    val = os.getenv(name)
    return val if val is not None else default


def _env_int(name: str, default: int | None = None) -> int | None:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _env_bool(name: str, default: bool = False) -> bool:
    return _to_bool(os.getenv(name), default)


# ----------------------------
# Config Classes
# ----------------------------
class BaseConfig:
    # Application Settings
    TIMEZONE = _env_str("TIMEZONE", DEFAULT_TIMEZONE)
    CURRENCY = _env_str("CURRENCY", DEFAULT_CURRENCY)
    DATE_FORMAT = _env_str("DATE_FORMAT", DEFAULT_DATE_FORMAT)
    TIME_FORMAT = _env_str("TIME_FORMAT", DEFAULT_TIME_FORMAT)
    LANGUAGE = _env_str("LANGUAGE", DEFAULT_LANGUAGE)
    BABEL_DEFAULT_LOCALE = _env_str("BABEL_DEFAULT_LOCALE", DEFAULT_BABEL_LOCALE)
    INITIAL_SETUP_COMPLETED = _env_bool("INITIAL_SETUP_COMPLETED", False)

    # Flask Settings
    DEBUG = False
    TESTING = False

    # Flask-SQLAlchemy Settings
    DATABASE_URL = _env_str("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = (
        DATABASE_URL if DATABASE_URL else f"sqlite:///{BASE_DIR / DEFAULT_SQLITE_FILENAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail Settings
    MAIL_SERVER = _env_str("MAIL_SERVER")
    MAIL_PORT = _env_int("MAIL_PORT")
    MAIL_USERNAME = _env_str("MAIL_USERNAME")
    MAIL_PASSWORD = _env_str("MAIL_PASSWORD")
    MAIL_USE_TLS = _env_bool("MAIL_USE_TLS", False)
    MAIL_USE_SSL = _env_bool("MAIL_USE_SSL", False)
    MAIL_DEFAULT_SENDER = _env_str("MAIL_DEFAULT_SENDER")
    MAIL_SUPPRESS_SEND = _env_bool("MAIL_SUPPRESS_SEND", False)

    # Secret Key
    _secret_from_env = _env_str("SECRET_KEY")
    SECRET_KEY = _secret_from_env or None

    @classmethod
    def validate(cls) -> None:
        # Enforce SECRET_KEY in production-like configs
        if not cls.SECRET_KEY and not (cls.DEBUG or cls.TESTING):
            raise RuntimeError(
                "Production SECRET_KEY must be configured via environment variable (.env). "
                "Set the SECRET_KEY environment variable with a secure value."
            )


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    # Development can fall back to the default dev secret if not provided
    SECRET_KEY = BaseConfig._secret_from_env or DEFAULT_DEV_SECRET
    MAIL_SUPPRESS_SEND = _env_bool("MAIL_SUPPRESS_SEND", True)
    INITIAL_SETUP_COMPLETED = True


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    # Testing can fall back to the default dev secret if not provided
    SECRET_KEY = BaseConfig._secret_from_env or DEFAULT_DEV_SECRET
    # Use in-memory SQLite for tests unless DATABASE_URL provided
    SQLALCHEMY_DATABASE_URI = (
        BaseConfig.DATABASE_URL if BaseConfig.DATABASE_URL else "sqlite:///:memory:"
    )
    MAIL_SUPPRESS_SEND = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    # Must be provided via env; BaseConfig.validate will enforce
    SECRET_KEY = BaseConfig._secret_from_env

    @classmethod
    def validate(cls) -> None:
        super().validate()


# Optional mapping helper
CONFIG_BY_NAME = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

# Validate the currently selected config
CONFIG_BY_NAME.get(os.getenv("FLASK_ENV", "development"), DevelopmentConfig).validate()
