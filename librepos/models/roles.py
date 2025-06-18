from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from librepos.extensions import db
from librepos.utils import timezone_aware_datetime

if TYPE_CHECKING:
    from librepos.models.users import User
    from librepos.models.role_policies import RolePolicy


class Role(db.Model):
    """Role model."""

    __tablename__ = "roles"

    def __init__(self, name: str, description: str, **kwargs):
        super(Role, self).__init__(**kwargs)
        """Create instance."""
        self.name = name.lower()
        self.description = description.lower()
        self.created_at = timezone_aware_datetime()

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]
    created_at: Mapped[datetime]
    active: Mapped[bool] = mapped_column(default=True)

    # Relationships
    users: Mapped[List["User"]] = relationship(back_populates="role")
    role_policies: Mapped[List["RolePolicy"]] = relationship(
        "RolePolicy", back_populates="role", cascade="all, delete-orphan"
    )

    def has_permission(self, permission_name: str) -> bool:
        """Check if any attached policy includes the permission."""
        for rp in self.role_policies:
            if rp.policy and rp.policy.has_permission(permission_name):
                return True
        return False
