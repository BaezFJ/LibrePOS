from datetime import datetime
from typing import Optional, List

from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash

from librepos.main.extensions import db
from librepos.utils.datetime import timezone_aware_datetime

iam_group_permissions = db.Table(
    "iam_group_permissions",
    db.Column("group_id", db.Integer, db.ForeignKey("iam_group.id"), primary_key=True),
    db.Column(
        "permission_id",
        db.Integer,
        db.ForeignKey("iam_permission.id"),
        primary_key=True,
    ),
)

iam_user_groups = db.Table(
    "iam_user_groups",
    db.Column("user_id", db.Integer, db.ForeignKey("iam_user.id"), primary_key=True),
    db.Column("group_id", db.Integer, db.ForeignKey("iam_group.id"), primary_key=True),
)

iam_user_permissions = db.Table(
    "iam_user_permissions",
    db.Column("user_id", db.Integer, db.ForeignKey("iam_user.id"), primary_key=True),
    db.Column(
        "permission_id",
        db.Integer,
        db.ForeignKey("iam_permission.id"),
        primary_key=True,
    ),
)


class IAMGroup(db.Model):
    """Auth group model."""

    def __init__(self, name: str, **kwargs):
        super(IAMGroup, self).__init__(**kwargs)
        self.name = name
        self.created_at = timezone_aware_datetime()

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[Optional[str]]
    created_at: Mapped[datetime]
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        onupdate=timezone_aware_datetime()
    )

    # Relationships
    permissions: Mapped[List["IAMPermission"]] = relationship(
        secondary=iam_group_permissions, back_populates="groups"
    )
    users: Mapped[List["IAMUser"]] = relationship(
        secondary=iam_user_groups, back_populates="groups"
    )


class IAMUser(UserMixin, db.Model):
    """Auth user model."""

    def __init__(self, username: str, password: str, **kwargs):
        super(IAMUser, self).__init__(**kwargs)
        self.username = username
        self.password = generate_password_hash(password)
        self.created_at = timezone_aware_datetime()

    # Columns
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    email: Mapped[Optional[str]] = mapped_column(unique=True, index=True)
    image: Mapped[Optional[str]] = mapped_column(nullable=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    failed_login_count: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime]
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        onupdate=timezone_aware_datetime()
    )

    # Relationships
    permissions: Mapped[List["IAMPermission"]] = relationship(
        secondary=iam_user_permissions, back_populates="users"
    )
    groups: Mapped[List["IAMGroup"]] = relationship(
        secondary=iam_user_groups, back_populates="users"
    )


class IAMPermission(db.Model):
    """Auth permission model."""

    def __init__(self, name: str, description: str, **kwargs):
        super(IAMPermission, self).__init__(**kwargs)
        self.name = name
        self.description = description
        self.created_at = timezone_aware_datetime()

    # Foreign keys
    created_by_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey("iam_user.id"))

    # Columns
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        onupdate=timezone_aware_datetime()
    )

    # Relationships
    groups: Mapped[List["IAMGroup"]] = relationship(
        secondary=iam_group_permissions, back_populates="permissions"
    )
    users: Mapped[List["IAMUser"]] = relationship(
        secondary=iam_user_permissions, back_populates="permissions"
    )
