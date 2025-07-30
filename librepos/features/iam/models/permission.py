from typing import List
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from librepos.extensions import db

if TYPE_CHECKING:
    from .policy_permission import PolicyPermission


class Permission(db.Model):
    """Permission model."""

    __tablename__ = "permissions"

    def __init__(self, name: str, **kwargs):
        super(Permission, self).__init__(**kwargs)
        """Create instance."""
        self.name = name.lower()

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]

    policy_permissions: Mapped[List["PolicyPermission"]] = relationship(
        "PolicyPermission", back_populates="permission", cascade="all, delete-orphan"
    )
