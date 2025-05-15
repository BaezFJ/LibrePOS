from typing import List

from sqlalchemy.orm import Mapped, relationship

from librepos.extensions import db
from librepos.utils import timezone_aware_datetime

from .policy_permissions import PolicyPermission


class Permission(db.Model):
    """Permission model."""

    __tablename__ = "permissions"

    def __init__(self, name: str, **kwargs):
        super(Permission, self).__init__(**kwargs)
        """Create instance."""
        self.name = name.lower()
        self.created_at = timezone_aware_datetime()

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)

    policy_permissions: Mapped[List["PolicyPermission"]] = relationship(
        "PolicyPermission", back_populates="permission", cascade="all, delete-orphan"
    )
