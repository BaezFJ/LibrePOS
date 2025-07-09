from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from librepos.extensions import db
from librepos.utils import timezone_aware_datetime

if TYPE_CHECKING:
    from .role import Role
    from .policy import Policy


# Association table with metadata: role <-> policy
class RolePolicy(db.Model):
    """RolePolicy model: Association table with metadata: role <-> policy"""

    __tablename__ = "role_policies"

    def __init__(self, role_id: int, policy_id: int, **kwargs):
        super(RolePolicy, self).__init__(**kwargs)
        self.assignee_id = kwargs.get("assignee_id", None)
        """Create instance."""
        self.role_id = role_id
        self.policy_id = policy_id
        self.assigned_at = timezone_aware_datetime()

    # ForeignKeys
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    policy_id: Mapped[int] = mapped_column(ForeignKey("policies.id"), primary_key=True)
    assignee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))

    # Columns
    assigned_at: Mapped[datetime]

    # Relationships
    role: Mapped["Role"] = relationship(back_populates="role_policies")
    policy: Mapped["Policy"] = relationship(back_populates="role_policies")
