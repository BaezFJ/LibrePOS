from datetime import datetime
from typing import List, TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from librepos.extensions import db
from librepos.utils import timezone_aware_datetime

if TYPE_CHECKING:
    from .menu_group import MenuGroup
    from librepos.features.iam.models import User


class MenuCategory(db.Model):
    """MenuCategory model."""

    __tablename__ = "menu_categories"

    def __init__(self, name: str, **kwargs):
        super(MenuCategory, self).__init__(**kwargs)
        self.name = name.capitalize()
        self.created_at = timezone_aware_datetime()

    # ForeignKeys
    created_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    updated_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[Optional[str]]
    active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime]
    updated_at: Mapped[Optional[datetime]]

    # Relationships
    menu_groups: Mapped[List["MenuGroup"]] = relationship(back_populates="category")
    created_by: Mapped["User"] = relationship(
        "User", back_populates="created_menu_categories", foreign_keys=[created_by_id]
    )
    updated_by: Mapped["User"] = relationship(
        "User", back_populates="updated_menu_categories", foreign_keys=[updated_by_id]
    )
