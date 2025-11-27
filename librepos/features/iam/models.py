from typing import Optional, List

from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash

from librepos.core.extensions import db
from librepos.core.database import BaseModel
from librepos.utils.datetime import timezone_aware_datetime

iam_group_permissions_association = db.Table(
    "iam_group_permissions_association",
    db.Column("group_id", db.Integer, db.ForeignKey("iam_group.id"), primary_key=True),
    db.Column(
        "permission_id",
        db.Integer,
        db.ForeignKey("iam_permission.id"),
        primary_key=True,
    ),
)

iam_user_groups_association = db.Table(
    "iam_user_groups_association",
    db.Column("user_id", db.Integer, db.ForeignKey("iam_user.id"), primary_key=True),
    db.Column("group_id", db.Integer, db.ForeignKey("iam_group.id"), primary_key=True),
)

iam_user_permissions_association = db.Table(
    "iam_user_permissions_association",
    db.Column("user_id", db.Integer, db.ForeignKey("iam_user.id"), primary_key=True),
    db.Column(
        "permission_id",
        db.Integer,
        db.ForeignKey("iam_permission.id"),
        primary_key=True,
    ),
)


class IAMGroup(BaseModel):
    """IAM group model."""

    __tablename__ = "iam_group"

    def __init__(self, name: str, **kwargs):
        super(IAMGroup, self).__init__(**kwargs)
        self.name = name
        self.created_at = timezone_aware_datetime()

    # id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[Optional[str]]
    # created_at: Mapped[datetime]
    # updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=timezone_aware_datetime())

    # Relationships
    permissions: Mapped[List["IAMPermission"]] = relationship(
        secondary=iam_group_permissions_association, back_populates="groups"
    )
    users: Mapped[List["IAMUser"]] = relationship(
        secondary=iam_user_groups_association, back_populates="groups"
    )


class IAMUser(UserMixin, BaseModel):
    """IAM user model."""

    __tablename__ = "iam_user"

    def __init__(self, username: str, password: str, **kwargs):
        super(IAMUser, self).__init__(**kwargs)
        self.username = username
        self.password = generate_password_hash(password)
        self.created_at = timezone_aware_datetime()

    # Columns
    # id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)
    failed_login_count: Mapped[int] = mapped_column(default=0)
    # created_at: Mapped[datetime]
    # updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=timezone_aware_datetime())

    # Relationships
    permissions: Mapped[List["IAMPermission"]] = relationship(
        secondary=iam_user_permissions_association, back_populates="users"
    )
    groups: Mapped[List["IAMGroup"]] = relationship(
        secondary=iam_user_groups_association, back_populates="users"
    )
    profile: Mapped["IAMUserProfile"] = relationship(
        "IAMUserProfile", uselist=False, back_populates="user"
    )

    def has_permission(self, permission_name: str) -> bool:
        """Check if the user has direct permission or through a group."""
        # Check user permissions
        if any(perm.name == permission_name for perm in self.permissions):
            return True
        # Check group permissions
        for group in self.groups:
            if any(perm.name == permission_name for perm in group.permissions):
                return True
        return False


class IAMUserProfile(BaseModel):
    """IAM user profile model."""

    __tablename__ = "iam_user_profile"

    def __init__(self, user_id, first_name: str, last_name: str, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = timezone_aware_datetime()

    # ForeignKeys
    user_id: Mapped[int] = mapped_column(db.ForeignKey("iam_user.id"))

    # Columns
    # id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    first_name: Mapped[str]
    middle_name: Mapped[Optional[str]]
    last_name: Mapped[str]
    image: Mapped[Optional[str]]
    email: Mapped[Optional[str]] = mapped_column(unique=True, index=True)
    # created_at: Mapped[datetime]
    # updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=timezone_aware_datetime())

    # Relationships
    user: Mapped["IAMUser"] = relationship("IAMUser", back_populates="profile")


class IAMPermissionCategory(BaseModel):
    """IAM permission category model."""

    __tablename__ = "iam_permission_category"

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.created_at = timezone_aware_datetime()

    # Columns
    # id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    # created_at: Mapped[datetime]
    # updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=timezone_aware_datetime())

    # Relationships
    permissions: Mapped[List["IAMPermission"]] = relationship(back_populates="category")


class IAMPermission(BaseModel):
    """IAM permission model."""

    __tablename__ = "iam_permission"

    def __init__(self, category_id: int, name: str, description: str, **kwargs):
        super(IAMPermission, self).__init__(**kwargs)
        self.category_id = category_id
        self.name = name
        self.description = description
        self.created_at = timezone_aware_datetime()

    # ForeignKey
    category_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey("iam_permission_category.id"))
    category: Mapped["IAMPermissionCategory"] = relationship(
        "IAMPermissionCategory", back_populates="permissions"
    )

    # Columns
    # id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]
    # created_at: Mapped[datetime]
    # updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=timezone_aware_datetime())

    # Relationships
    groups: Mapped[List["IAMGroup"]] = relationship(
        secondary=iam_group_permissions_association, back_populates="permissions"
    )
    users: Mapped[List["IAMUser"]] = relationship(
        secondary=iam_user_permissions_association, back_populates="permissions"
    )
