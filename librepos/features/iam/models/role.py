from datetime import datetime
from typing import List, Optional
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from librepos.extensions import db
from librepos.utils import timezone_aware_datetime
from .associations import role_permission_association

if TYPE_CHECKING:
    from .user import User
    from .permission import Permission


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
    updated_at: Mapped[Optional[datetime]]
    active: Mapped[bool] = mapped_column(default=True)
    deletable: Mapped[bool] = mapped_column(default=True)

    # Relationships
    users: Mapped[List["User"]] = relationship(back_populates="role")
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary=role_permission_association,
        back_populates="roles",
        lazy="joined",
    )

    def has_permission(self, permission_name: str) -> bool:
        """Check if any attached policy includes the permission."""
        return any(p.name == permission_name for p in self.permissions)
