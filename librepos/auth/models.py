from typing import Optional

from flask_login import UserMixin
from slugify import slugify
from sqlalchemy import ForeignKey
from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy.orm import Mapped, mapped_column, relationship

from librepos.extensions import db, AssociationModel
from librepos.utils.sqlalchemy import CRUDMixin
from .config import Permissions, Roles


class AuthPermission(CRUDMixin, db.Model):
    __tablename__ = "auth_permission"
    # **************** Columns ****************
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]]

    # ************** Relationships ****************
    role_permissions: Mapped[list["AuthRolePermission"]] = relationship(
        foreign_keys=lambda: [
            AuthRolePermission.permission_id
        ],  # ✅ Use lambda for delayed evaluation
        back_populates="permission",
    )

    # Use association proxy for convenient access to roles
    @property
    def roles(self) -> list["AuthRole"]:
        """Get all roles that have this permission."""
        return [rp.role for rp in self.role_permissions]

    SEED_DATA = Permissions

    def __init__(self, name: str, **kwargs):
        super(AuthPermission, self).__init__(**kwargs)
        self.name = name


class AuthRolePermission(CRUDMixin, AssociationModel):
    __tablename__ = "auth_role_permission"
    # **************** Columns ****************
    role_id: Mapped[int] = mapped_column(ForeignKey("auth_role.id"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("auth_permission.id"), primary_key=True)
    added_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("auth_user.id"), nullable=True)

    # **************** Relationships ****************
    added_by: Mapped[Optional["AuthUser"]] = relationship(foreign_keys=[added_by_id])
    role: Mapped["AuthRole"] = relationship(back_populates="role_permissions")
    permission: Mapped["AuthPermission"] = relationship(back_populates="role_permissions")

    def __init__(self, role_id: int, permission_id: int, **kwargs):
        super().__init__(**kwargs)
        self.role_id = role_id
        self.permission_id = permission_id


class AuthRole(CRUDMixin, db.Model):
    __tablename__ = "auth_role"
    # **************** Columns ****************
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]]
    is_system: Mapped[bool] = mapped_column(default=False)

    # **************** Relationships ****************
    users: Mapped[list["AuthUser"]] = relationship(back_populates="role")
    role_permissions: Mapped[list["AuthRolePermission"]] = relationship(
        foreign_keys=lambda: [AuthRolePermission.role_id],  # ✅ Use lambda for delayed evaluation
        back_populates="role",
    )

    # Use association proxy for convenient access to permissions
    @property
    def permissions(self) -> list["AuthPermission"]:
        """Get all permissions associated with this role."""
        return [rp.permission for rp in self.role_permissions]

    SEED_DATA = Roles

    def __init__(self, name: str, **kwargs):
        super(AuthRole, self).__init__(**kwargs)
        self.name = name
        self.slug = slugify(name)


class AuthUser(UserMixin, CRUDMixin, db.Model):
    __tablename__ = "auth_user"
    # **************** Columns ****************
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    middle_name: Mapped[Optional[str]]
    last_name: Mapped[str] = mapped_column(nullable=False)

    # **************** Foreign Keys ****************
    role_id: Mapped[Optional[int]] = mapped_column(ForeignKey("auth_role.id"))

    # ************** Reverse Relationships ****************
    role: Mapped[Optional["AuthRole"]] = relationship(back_populates="users")

    def __init__(self, username: str, email: str, unsecure_password: str, **kwargs):
        super(AuthUser, self).__init__(**kwargs)
        self.username = username
        self.slug = slugify(username)
        self.email = email
        self.set_password(unsecure_password)

    def set_password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(str(self.hashed_password), password)

    def has_permission(self, permission_name: str) -> bool:
        """Check if the user's role has a given permission.

        Args:
            permission_name: Name of the permission to check for

        Returns:
            bool: True if the user's role has the permission, False otherwise
        """
        if not self.role:
            return False
        return any(perm.name == permission_name for perm in self.role.permissions)

    @property
    def fullname(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
