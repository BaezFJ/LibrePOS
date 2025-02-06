import enum
from typing import cast, List, Any

from flask_login import UserMixin
from sqlalchemy import Enum
from werkzeug.security import check_password_hash, generate_password_hash

from librepos.extensions import db
from librepos.utils.helpers import (
    dollars_to_cents,
    generate_password,
    generate_slug,
    generate_token,
    generate_uuid,
    timezone_aware_datetime,
)
from librepos.utils.sqlalchemy import CRUDMixin, TimestampMixin


class UserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    FIRED = "fired"
    PENDING = "pending"
    DELETED = "deleted"


class User(UserMixin, CRUDMixin, TimestampMixin, db.Model):
    def __init__(self, username, email, first_name, last_name, **kwargs):
        super(User, self).__init__(**kwargs)

        self.id = generate_uuid()
        self.username = username
        self.slug = generate_slug(username)
        self.email = email
        self.api_token = generate_token()
        self.first_name = first_name.capitalize()
        self.last_name = last_name.capitalize()

        if kwargs.get("password_hash"):
            self.set_password(kwargs.get("password_hash"))
        else:
            temporary_password = generate_password()
            self.set_password(temporary_password)
            # TODO 1/28/25 : make a function to send the temporary password to user preferred method email/phone

    # ForeignKeys
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)

    # Columns
    id = db.Column(db.String, primary_key=True, unique=True, index=True)
    slug = db.Column(db.String(30), unique=True, index=True)
    hourly_rate = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(Enum(UserStatus), nullable=False, default=UserStatus.ACTIVE)

    # Authentication
    username = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    api_token = db.Column(db.String(128), unique=True, index=True)

    # Contact
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, index=True)
    phone = db.Column(db.String(15), nullable=True, index=True)
    phone_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    role = db.relationship("Role", back_populates="users")

    # Relationship for group membership (via the association model)
    group_users = db.relationship(
        "GroupUser", back_populates="user", cascade="all, delete-orphan"
    )

    @property
    def is_active(self):
        return self.status == UserStatus.ACTIVE

    @property
    def last_activity(self):
        # return self.orders[-1].created_at if self.orders else None
        return timezone_aware_datetime().date()

    @property
    def groups(self) -> List[Any]:
        """Returns a list of groups the user belongs to."""
        _group_users = cast(List[Any], self.group_users)
        return [gu.group for gu in _group_users]

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

    @classmethod
    def get_by_identity(cls, identity: str):
        """Get a user by username or email."""
        return cls.query.filter((cls.username == identity) | (cls.email == identity))

    def set_password(self, password):
        """Set the user's password."""
        self.password_hash = generate_password_hash(
            password, salt_length=32, method="pbkdf2:sha256:80000"
        )

    def check_password(self, password):
        """Check if the user's password is correct."""
        return check_password_hash(self.password_hash, password)

    def set_hourly_rate(self, new_rate):
        """Update the user's hourly rate."""
        self.hourly_rate = dollars_to_cents(new_rate)
        db.session.commit()
