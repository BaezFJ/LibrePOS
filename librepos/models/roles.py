from typing import List

from sqlalchemy.orm import Mapped, relationship

from librepos.extensions import db
from librepos.utils import timezone_aware_datetime

from .role_policies import RolePolicy


class Role(db.Model):
    """Role model."""

    __tablename__ = "roles"

    def __init__(self, name: str, description: str):
        super(Role, self).__init__()
        """Create instance."""
        self.name = name.lower()
        self.description = description.lower()
        self.created_at = timezone_aware_datetime()

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    users = db.relationship("User", back_populates="role")
    role_policies: Mapped[List["RolePolicy"]] = relationship(
        "RolePolicy", back_populates="role", cascade="all, delete-orphan"
    )

    def has_permission(self, permission_name: str) -> bool:
        """Check if any attached policy includes the permission."""
        for rp in self.role_policies:
            if rp.policy and rp.policy.has_permission(permission_name):
                return True
        return False
