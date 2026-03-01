"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """Base configuration with shared settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Core Flask settings
    SECRET_KEY: str | None = None
    DEBUG: bool = False
    TESTING: bool = False

    # Database
    SQLALCHEMY_DATABASE_URI: str | None = None
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # Session security
    SESSION_COOKIE_SECURE: bool = False

    # Application
    BUSINESS_NAME: str = "LibrePOS"
    APP_NAME: str = "LibrePOS"
    INITIAL_SETUP_COMPLETED: bool = False

    # Mail settings (Flask-Mailman)
    MAIL_SERVER: str | None = None
    MAIL_PORT: int = 587
    MAIL_USERNAME: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_USE_TLS: bool = True
    MAIL_USE_SSL: bool = False
    MAIL_DEFAULT_SENDER: str | None = None
    MAIL_SUPPRESS_SEND: bool = False

    @classmethod
    def init_app(cls) -> None:
        """Validate configuration at app startup.

        Creates an instance to trigger pydantic validation.
        Override in subclasses for environment-specific checks.
        """
        instance = cls()
        if not instance.SECRET_KEY:
            raise ValueError("SECRET_KEY is required")
        if not instance.TESTING and not instance.SQLALCHEMY_DATABASE_URI:
            raise ValueError("SQLALCHEMY_DATABASE_URI is required")


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG: bool = True
    SECRET_KEY: str = "development-secret-key"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./dev.db"


class TestingConfig(BaseConfig):
    """Testing configuration with in-memory SQLite."""

    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
    SECRET_KEY: str = "test-secret-key-not-for-production"
    INITIAL_SETUP_COMPLETED: bool = True

    @classmethod
    def init_app(cls) -> None:
        """Skip database URI validation for testing."""


class ProductionConfig(BaseConfig):
    """Production configuration with secure defaults."""

    SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "Lax"


CONFIG_BY_NAME: dict[str, type[BaseConfig]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
