import enum
from typing import cast, List, Any

from flask_login import UserMixin
from sqlalchemy import Enum
from werkzeug.security import check_password_hash, generate_password_hash

from librepos.extensions import db
from librepos.utils.helpers import (
    generate_uuid, timezone_aware_datetime
)
from librepos.utils.sqlalchemy import CRUDMixin, TimestampMixin


class UserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    FIRED = "fired"
    PENDING = "pending"
    DELETED = "deleted"
    LOCKED = "locked"


class User(UserMixin, CRUDMixin, TimestampMixin, db.Model):
    def __init__(self, role_id, username, password, **kwargs):
        super(User, self).__init__(**kwargs)

        self.id = generate_uuid()
        self.role_id = role_id
        self.username = username

        self.set_password(password)
        self.init_relationships()

    # ForeignKeys
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)

    # Columns
    id = db.Column(db.String, primary_key=True, unique=True, index=True)
    status = db.Column(Enum(UserStatus), nullable=False, default=UserStatus.ACTIVE)
    password_hash = db.Column(db.String(128))
    username = db.Column(db.String(120), unique=True, index=True)

    # Relationships
    role = db.relationship("Role", back_populates="users")
    profile = db.relationship("UserProfile", back_populates="user", uselist=False)
    activity = db.relationship("UserActivity", back_populates="user", uselist=False)
    addresses = db.relationship("UserAddress", back_populates="user")
    shift_details = db.relationship("UserShiftDetails", back_populates="user")
    work_details = db.relationship("UserWorkDetails", back_populates="user", uselist=False)

    # Relationship for group membership (via the association model)
    group_users = db.relationship(
        "GroupUser", back_populates="user", cascade="all, delete-orphan"
    )

    @property
    def is_active(self):
        return self.status == UserStatus.ACTIVE

    @property
    def phone(self):
        return self.profile.phone_number if self.profile else None

    @property
    def groups(self) -> List[Any]:
        """Returns a list of groups the user belongs to."""
        _group_users = cast(List[Any], self.group_users)
        return [gu.group for gu in _group_users]

    def init_relationships(self):
        from librepos.blueprints.user.models import UserProfile, UserActivity, UserWorkDetails

        # UserProfile.create(user=self)
        UserActivity.create(user=self)
        # UserWorkDetails.create(user=self, user_id=self.id, start_date=timezone_aware_datetime().date(),
        #                        hire_date=timezone_aware_datetime().date(), start_compensation=1500)

    def change_status(self, status: UserStatus):
        self.status = status
        db.session.commit()

    def has_permission(self, permission_name: str) -> bool:
        """
        Check if the user has a specific permission.
        This method iterates over the user's groups, then for each group,
        iterates over its policies, and finally checks if any of those policies
        grant the specified permission.

        :param permission_name: The name of the permission to check.
        :return: True if the permission is found, otherwise False.
        """
        for group in self.groups:
            # group.policies is a convenience property returning policies via PolicyGroup
            for policy in group.policies:
                # policy.permissions returns permissions via PermissionPolicy
                for permission in policy.permissions:
                    if permission.name == permission_name:
                        return True
        return False

    def list_permissions(self):
        """
        Retrieve all unique permissions for this user based on group -> policy -> permission relationships.

        :return: A list of unique Permission objects.
        """
        permissions_dict = {}
        # Iterate over each group the user belongs to.
        for group in self.groups:
            # Each group has a list of policies (via the PolicyGroup association)
            for policy in group.policies:
                # Each policy has a list of permissions (via the PermissionPolicy association)
                for permission in policy.permissions:
                    permissions_dict[permission.id] = permission
        return list(permissions_dict.values())

    def list_policies(self):
        policies_dict = {}
        for group in self.groups:
            for policy in group.policies:
                policies_dict[policy.id] = policy
        return list(policies_dict.values())

    def set_password(self, password):
        """Set the user's password."""
        self.password_hash = generate_password_hash(
            password, salt_length=32, method="pbkdf2:sha256:80000"
        )

    def check_password(self, password):
        """Check if the user's password is correct."""
        return check_password_hash(self.password_hash, password)
