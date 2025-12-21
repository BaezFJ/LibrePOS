from typing import Optional

from flask_login import UserMixin
from slugify import slugify
from sqlalchemy import ForeignKey
from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy.orm import Mapped, mapped_column, relationship

from librepos.extensions import db, AssociationModel
from librepos.utils.sqlalchemy import CRUDMixin


class IAMPermission(CRUDMixin, db.Model):
    __tablename__ = "iam_permission"
    # **************** Columns ****************
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]]

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
        super(IAMPermission, self).__init__(**kwargs)
        self.name = name


class IAMPolicyPermission(CRUDMixin, AssociationModel):
    __tablename__ = "iam_policy_permission"
    # **************** Columns ****************
    policy_id: Mapped[int] = mapped_column(ForeignKey("iam_policy.id"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("iam_permission.id"), primary_key=True)
    added_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("iam_user.id"), nullable=True)

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
    description: Mapped[Optional[str]]
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
        super(IAMPolicy, self).__init__(**kwargs)
        self.name = name
        self.slug = slugify(name)


class IAMRolePermission(CRUDMixin, AssociationModel):
    __tablename__ = "iam_role_permission"
    # **************** Columns ****************
    role_id: Mapped[int] = mapped_column(ForeignKey("iam_role.id"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("iam_permission.id"), primary_key=True)
    added_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("iam_user.id"), nullable=True)

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
    added_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("iam_user.id"), nullable=True)

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
    slug: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]]
    is_system: Mapped[bool] = mapped_column(default=False)

    # **************** Relationships ****************
    group_roles: Mapped[list["IAMGroupRole"]] = relationship(
        foreign_keys=lambda: [IAMGroupRole.role_id],
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
    def groups(self) -> list["IAMGroup"]:
        """Get all groups that have this role."""
        return [gr.group for gr in self.group_roles]

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
        super(IAMRole, self).__init__(**kwargs)
        self.name = name
        self.slug = slugify(name)


class IAMGroupRole(CRUDMixin, AssociationModel):
    __tablename__ = "iam_group_role"
    # **************** Columns ****************
    group_id: Mapped[int] = mapped_column(ForeignKey("iam_group.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("iam_role.id"), primary_key=True)
    added_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("iam_user.id"), nullable=True)

    # **************** Relationships ****************
    added_by: Mapped[Optional["IAMUser"]] = relationship(foreign_keys=[added_by_id])
    group: Mapped["IAMGroup"] = relationship(back_populates="group_roles")
    role: Mapped["IAMRole"] = relationship(back_populates="group_roles")

    def __init__(self, group_id: int, role_id: int, **kwargs):
        super().__init__(**kwargs)
        self.group_id = group_id
        self.role_id = role_id


class IAMGroup(CRUDMixin, db.Model):
    __tablename__ = "iam_group"
    # **************** Columns ****************
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]]

    # **************** Relationships ****************
    user_groups: Mapped[list["IAMUserGroup"]] = relationship(
        foreign_keys=lambda: [IAMUserGroup.group_id],
        back_populates="group",
    )
    group_roles: Mapped[list["IAMGroupRole"]] = relationship(
        foreign_keys=lambda: [IAMGroupRole.group_id],
        back_populates="group",
    )

    @property
    def users(self) -> list["IAMUser"]:
        """Get all users in this group."""
        return [ug.user for ug in self.user_groups]

    @property
    def roles(self) -> list["IAMRole"]:
        """Get all roles assigned to this group."""
        return [gr.role for gr in self.group_roles]

    def __init__(self, name: str, **kwargs):
        super(IAMGroup, self).__init__(**kwargs)
        self.name = name
        self.slug = slugify(name)


class IAMUserGroup(CRUDMixin, AssociationModel):
    __tablename__ = "iam_user_group"
    # **************** Columns ****************
    user_id: Mapped[int] = mapped_column(ForeignKey("iam_user.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("iam_group.id"), primary_key=True)
    added_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("iam_user.id"), nullable=True)

    # **************** Relationships ****************
    added_by: Mapped[Optional["IAMUser"]] = relationship(foreign_keys=[added_by_id])
    user: Mapped["IAMUser"] = relationship(
        foreign_keys=[user_id],
        back_populates="user_groups",
    )
    group: Mapped["IAMGroup"] = relationship(back_populates="user_groups")

    def __init__(self, user_id: int, group_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.group_id = group_id


class IAMUser(UserMixin, CRUDMixin, db.Model):
    __tablename__ = "iam_user"
    # **************** Columns ****************
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    middle_name: Mapped[Optional[str]]
    last_name: Mapped[str] = mapped_column(nullable=False)

    # ************** Relationships ****************
    user_groups: Mapped[list["IAMUserGroup"]] = relationship(
        foreign_keys=lambda: [IAMUserGroup.user_id],
        back_populates="user",
    )

    @property
    def groups(self) -> list["IAMGroup"]:
        """Get all groups this user belongs to."""
        return [ug.group for ug in self.user_groups]

    @property
    def roles(self) -> list["IAMRole"]:
        """Get all roles from all groups this user belongs to."""
        roles = []
        for group in self.groups:
            roles.extend(group.roles)
        return roles

    @property
    def permissions(self) -> list["IAMPermission"]:
        """Get all permissions from all roles across all groups."""
        permissions = []
        for role in self.roles:
            permissions.extend(role.permissions)
        return list(set(permissions))  # Remove duplicates

    def __init__(self, username: str, email: str, unsecure_password: str, **kwargs):
        super(IAMUser, self).__init__(**kwargs)
        self.username = username
        self.slug = slugify(username)
        self.email = email
        self.set_password(unsecure_password)

    def set_password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(str(self.hashed_password), password)

    def has_permission(self, permission_name: str) -> bool:
        """Check if the user has a given permission through any of their groups' roles.

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
