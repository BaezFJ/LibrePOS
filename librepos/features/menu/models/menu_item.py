from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from librepos.extensions import db
from librepos.utils import timezone_aware_datetime

if TYPE_CHECKING:
    from .menu_group import MenuGroup
    from librepos.features.iam.models import User


class MenuItem(db.Model):
    """MenuItem model."""

    __tablename__ = "menu_items"

    def __init__(
        self, group_id: int, name: str, description: str, price: int, **kwargs
    ):
        super(MenuItem, self).__init__(**kwargs)
        """Create instance."""
        self.group_id = group_id
        self.name = name.title()
        self.description = description.capitalize()
        self.price = price
        self.created_at = timezone_aware_datetime()

    # ForeignKeys
    group_id: Mapped[int] = mapped_column(ForeignKey("menu_groups.id"))
    created_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    updated_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=False, index=True)
    description: Mapped[str]
    price: Mapped[int] = mapped_column(default=0)
    active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime]
    updated_at: Mapped[Optional[datetime]]

    # Relationships
    group: Mapped["MenuGroup"] = relationship(back_populates="menu_items")
    created_by: Mapped["User"] = relationship(
        "User", back_populates="created_menu_items", foreign_keys=[created_by_id]
    )
    updated_by: Mapped["User"] = relationship(
        "User", back_populates="updated_menu_items", foreign_keys=[updated_by_id]
    )

    @property
    def item_name_with_group(self):
        return f"{self.group.name} - {self.name}"
