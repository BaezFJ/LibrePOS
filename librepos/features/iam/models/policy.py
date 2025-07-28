from datetime import datetime
from typing import List
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from librepos.extensions import db
from librepos.utils import timezone_aware_datetime

if TYPE_CHECKING:
    from .role_policy import RolePolicy
    from .policy_permission import PolicyPermission


class Policy(db.Model):
    """Policy model."""

    __tablename__ = "policies"

    def __init__(self, name: str, description: str):
        super(Policy, self).__init__()
        """Create instance."""
        self.name = name
        self.description = description
        self.created_at = timezone_aware_datetime()

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]
    created_at: Mapped[datetime]
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

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
