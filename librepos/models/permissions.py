from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from librepos.extensions import db
from librepos.utils import timezone_aware_datetime

if TYPE_CHECKING:
    from librepos.models.policy_permissions import PolicyPermission


class Permission(db.Model):
    """Permission model."""

    __tablename__ = "permissions"

    def __init__(self, name: str, **kwargs):
        super(Permission, self).__init__(**kwargs)
        """Create instance."""
        self.name = name.lower()
        self.created_at = timezone_aware_datetime()

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    created_at: Mapped[datetime]
    active: Mapped[bool] = mapped_column(default=False)

    policy_permissions: Mapped[List["PolicyPermission"]] = relationship(
        "PolicyPermission", back_populates="permission", cascade="all, delete-orphan"
    )
