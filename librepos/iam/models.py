from enum import StrEnum
from typing import Optional

from flask_login import UserMixin
from slugify import slugify
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from librepos.extensions import AssociationModel, db
from librepos.utils.sqlalchemy import CRUDMixin


class UserStatus(StrEnum):
    ACTIVE = "active"
    PENDING = "pending"
    INVITED = "invited"
    SUSPENDED = "suspended"
    DEACTIVATED = "deactivated"
    LOCKED = "locked"
    DELETED = "deleted"


class IAMPermission(CRUDMixin, db.Model):
    __tablename__ = "iam_permission"
    # **************** Columns ****************
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    description: Mapped[str | None]

    # ************** Relationships ****************
    role_permissions: Mapped[list["IAMRolePermission"]] = relationship(
        foreign_keys=lambda: [IAMRolePermission.permission_id],
        back_populates="permission",
    )
    policy_permissions: Mapped[list["IAMPolicyPermission"]] = relationship(
        foreign_keys=lambda: [IAMPolicyPermission.permission_id],
        back_populates="permission",
    )

    @property
    def roles(self) -> list["IAMRole"]:
        """Get all roles that have this permission."""
        return [rp.role for rp in self.role_permissions]

    @property
    def policies(self) -> list["IAMPolicy"]:
        """Get all policies that have this permission."""
        return [pp.policy for pp in self.policy_permissions]

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name


class IAMPolicyPermission(CRUDMixin, AssociationModel):
    __tablename__ = "iam_policy_permission"
    # **************** Columns ****************
    policy_id: Mapped[int] = mapped_column(ForeignKey("iam_policy.id"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("iam_permission.id"), primary_key=True)
    added_by_id: Mapped[int | None] = mapped_column(ForeignKey("iam_user.id"), nullable=True)

    # **************** Relationships ****************
    added_by: Mapped[Optional["IAMUser"]] = relationship(foreign_keys=[added_by_id])
    policy: Mapped["IAMPolicy"] = relationship(back_populates="policy_permissions")
    permission: Mapped["IAMPermission"] = relationship(back_populates="policy_permissions")

    def __init__(self, policy_id: int, permission_id: int, **kwargs):
        super().__init__(**kwargs)
        self.policy_id = policy_id
        self.permission_id = permission_id


class IAMPolicy(CRUDMixin, db.Model):
    __tablename__ = "iam_policy"
    # **************** Columns ****************
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    description: Mapped[str | None]
    is_system: Mapped[bool] = mapped_column(default=False)

    # **************** Relationships ****************
    policy_permissions: Mapped[list["IAMPolicyPermission"]] = relationship(
        foreign_keys=lambda: [IAMPolicyPermission.policy_id],
        back_populates="policy",
    )
    role_policies: Mapped[list["IAMRolePolicy"]] = relationship(
        foreign_keys=lambda: [IAMRolePolicy.policy_id],
        back_populates="policy",
    )

    @property
    def permissions(self) -> list["IAMPermission"]:
        """Get all permissions in this policy."""
        return [pp.permission for pp in self.policy_permissions]

    @property
    def roles(self) -> list["IAMRole"]:
        """Get all roles that have this policy."""
        return [rp.role for rp in self.role_policies]

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.slug = slugify(name)


class IAMRolePermission(CRUDMixin, AssociationModel):
    __tablename__ = "iam_role_permission"
    # **************** Columns ****************
    role_id: Mapped[int] = mapped_column(ForeignKey("iam_role.id"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("iam_permission.id"), primary_key=True)
    added_by_id: Mapped[int | None] = mapped_column(ForeignKey("iam_user.id"), nullable=True)

    # **************** Relationships ****************
    added_by: Mapped[Optional["IAMUser"]] = relationship(foreign_keys=[added_by_id])
    role: Mapped["IAMRole"] = relationship(back_populates="role_permissions")
    permission: Mapped["IAMPermission"] = relationship(back_populates="role_permissions")

    def __init__(self, role_id: int, permission_id: int, **kwargs):
        super().__init__(**kwargs)
        self.role_id = role_id
        self.permission_id = permission_id


class IAMRolePolicy(CRUDMixin, AssociationModel):
    __tablename__ = "iam_role_policy"
    # **************** Columns ****************
    role_id: Mapped[int] = mapped_column(ForeignKey("iam_role.id"), primary_key=True)
    policy_id: Mapped[int] = mapped_column(ForeignKey("iam_policy.id"), primary_key=True)
    added_by_id: Mapped[int | None] = mapped_column(ForeignKey("iam_user.id"), nullable=True)

    # **************** Relationships ****************
    added_by: Mapped[Optional["IAMUser"]] = relationship(foreign_keys=[added_by_id])
    role: Mapped["IAMRole"] = relationship(back_populates="role_policies")
    policy: Mapped["IAMPolicy"] = relationship(back_populates="role_policies")

    def __init__(self, role_id: int, policy_id: int, **kwargs):
        super().__init__(**kwargs)
        self.role_id = role_id
        self.policy_id = policy_id


class IAMRole(CRUDMixin, db.Model):
    __tablename__ = "iam_role"
    # **************** Columns ****************
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    is_staff_role: Mapped[bool] = mapped_column(default=False)
    slug: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    description: Mapped[str | None]
    is_system: Mapped[bool] = mapped_column(default=False)

    # **************** Relationships ****************
    users: Mapped[list["IAMUser"]] = relationship(
        back_populates="role",
    )
    role_permissions: Mapped[list["IAMRolePermission"]] = relationship(
        foreign_keys=lambda: [IAMRolePermission.role_id],
        back_populates="role",
    )
    role_policies: Mapped[list["IAMRolePolicy"]] = relationship(
        foreign_keys=lambda: [IAMRolePolicy.role_id],
        back_populates="role",
    )

    @property
    def permissions(self) -> list["IAMPermission"]:
        """Get all permissions associated with this role (both direct and from policies)."""
        perms = [rp.permission for rp in self.role_permissions]
        for policy in self.policies:
            perms.extend(policy.permissions)
        return perms

    @property
    def policies(self) -> list["IAMPolicy"]:
        """Get all policies assigned to this role."""
        return [rp.policy for rp in self.role_policies]

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.slug = slugify(name)


class IAMUser(UserMixin, CRUDMixin, db.Model):
    __tablename__ = "iam_user"

    # **************** Foreign Keys ****************
    role_id: Mapped[int | None] = mapped_column(ForeignKey("iam_role.id"), nullable=True)

    # **************** Columns ****************
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    middle_name: Mapped[str | None] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[UserStatus] = mapped_column(default=UserStatus.PENDING)

    # ************** Relationships ****************
    role: Mapped[Optional["IAMRole"]] = relationship(back_populates="users")

    @property
    def is_staff(self) -> bool:
        return self.role.is_staff_role if self.role else False

    @property
    def permissions(self) -> list["IAMPermission"]:
        """Get all permissions from the user's role."""
        if self.role:
            return self.role.permissions
        return []

    def __init__(self, username: str, email: str, unsecure_password: str, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.slug = slugify(username)
        self.email = email
        self.set_password(unsecure_password)

    def set_password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(str(self.hashed_password), password)

    def has_permission(self, permission_name: str) -> bool:
        """Check if the user has a given permission through their role.

        Args:
            permission_name: Name of the permission to check for

        Returns:
            bool: True if the user has the permission, False otherwise
        """
        return any(perm.name == permission_name for perm in self.permissions)

    @property
    def fullname(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
