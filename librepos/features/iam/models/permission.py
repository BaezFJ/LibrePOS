# from typing import List
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from librepos.extensions import db
from .associations import role_permission_association

if TYPE_CHECKING:
    from .role import Role


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

    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary=role_permission_association,
        back_populates="permissions",
        lazy="joined",
    )

    # policy_permissions: Mapped[List["PolicyPermission"]] = relationship(
    #     "PolicyPermission", back_populates="permission", cascade="all, delete-orphan"
    # )
