from datetime import datetime

from flask_mailman import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from librepos.app.shared.helpers import fetch_time_by_timezone


class Base(DeclarativeBase):
    """Shared base for all models to ensure a single registry."""


class TimestampMixin:
    """Mixin to add created_at and updated_at columns."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: fetch_time_by_timezone(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
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
migrate = Migrate()
mail = Mail()
csrf = CSRFProtect()


def init_extensions(app):
    """Initialize Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        db.create_all()
