from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from librepos.extensions import db
from librepos.utils import timezone_aware_datetime

if TYPE_CHECKING:
    from librepos.models.policies import Policy
    from librepos.models.permissions import Permission


# Association table with metadata: policy <-> permission
class PolicyPermission(db.Model):
    """PolicyPermission model: Association table with metadata: policy <-> permission"""

    __tablename__ = "policy_permissions"

    def __init__(self, policy_id: int, permission_id: int, added_by: str):
        super(PolicyPermission, self).__init__()
        """Create instance."""
        self.policy_id = policy_id
        self.permission_id = permission_id
        self.added_by = added_by.lower()
        self.added_at = timezone_aware_datetime()

    # ForeignKeys
    policy_id: Mapped[int] = mapped_column(ForeignKey("policies.id"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id"), primary_key=True
    )

    # Columns
    added_by: Mapped[str]
    added_at: Mapped[datetime]

    # Relationships
    policy: Mapped["Policy"] = relationship(back_populates="policy_permissions")
    permission: Mapped["Permission"] = relationship(back_populates="policy_permissions")
