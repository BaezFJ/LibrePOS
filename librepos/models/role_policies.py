from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from librepos.extensions import db
from librepos.utils import timezone_aware_datetime

if TYPE_CHECKING:
    from librepos.models.roles import Role
    from librepos.models.policies import Policy


# Association table with metadata: role <-> policy
class RolePolicy(db.Model):
    """RolePolicy model: Association table with metadata: role <-> policy"""

    __tablename__ = "role_policies"

    def __init__(self, role_id: int, policy_id: int, assigned_by: str):
        super(RolePolicy, self).__init__()
        """Create instance."""
        self.role_id = role_id
        self.policy_id = policy_id
        self.assigned_by = assigned_by.lower()
        self.assigned_at = timezone_aware_datetime()

    # ForeignKeys
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    policy_id: Mapped[int] = mapped_column(ForeignKey("policies.id"), primary_key=True)

    # Columns
    assigned_by: Mapped[str]
    assigned_at: Mapped[datetime]

    # Relationships
    role: Mapped["Role"] = relationship(back_populates="role_policies")
    policy: Mapped["Policy"] = relationship(back_populates="role_policies")
