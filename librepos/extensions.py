from flask_login import LoginManager
from datetime import datetime
from typing import Optional

from flask_mailman import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from librepos.utils.datetime import fetch_time_by_timezone


class Base(DeclarativeBase):
    """Shared base for all models to ensure a single registry."""

    pass


class TimestampMixin:
    """Mixin to add created_at and updated_at columns."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: fetch_time_by_timezone(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=lambda: fetch_time_by_timezone(),
        onupdate=lambda: fetch_time_by_timezone(),
    )


class BaseModel(Base, TimestampMixin):
    """Base model class for all database models."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)


class AssociationModel(Base, TimestampMixin):
    """Base model for association/junction tables without an id column."""

    __abstract__ = True


db = SQLAlchemy(model_class=BaseModel)
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()


def init_extensions(app):
    """Initialize Flask extensions."""
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    setattr(login_manager, "login_view", "auth.login")
    login_manager.session_protection = "strong"

    with app.app_context():
        # Import models so SQLAlchemy is aware of all tables before create_all
        # (avoid circular imports by importing locally)
        from librepos.auth import models as _iam_models  # noqa: F401
        from librepos.main import models as _main_models  # noqa: F401

        db.create_all()

        from librepos.auth.models import AuthRole, AuthPermission

        AuthPermission.seed_data()
        AuthRole.seed_data()

    @login_manager.user_loader
    def load_user(user_id):
        from librepos.auth.models import AuthUser

        return AuthUser.get_by_id(user_id)
