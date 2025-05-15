from typing import List

from sqlalchemy.orm import Mapped, relationship

from librepos.extensions import db
from librepos.utils import timezone_aware_datetime

from .role_policies import RolePolicy
from .policy_permissions import PolicyPermission


class Policy(db.Model):
    """Policy model."""

    __tablename__ = "policies"

    def __init__(self, name: str, description: str):
        super(Policy, self).__init__()
        """Create instance."""
        self.name = name.lower()
        self.description = description.lower()
        self.created_at = timezone_aware_datetime()

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False)

    # Relationships
    role_policies: Mapped[List["RolePolicy"]] = relationship(
        "RolePolicy", back_populates="policy", cascade="all, delete-orphan"
    )
    policy_permissions: Mapped[List["PolicyPermission"]] = relationship(
        "PolicyPermission", back_populates="policy", cascade="all, delete-orphan"
    )

    def has_permission(self, permission_name: str) -> bool:
        return any(
            pp.permission.name == permission_name for pp in self.policy_permissions
        )
