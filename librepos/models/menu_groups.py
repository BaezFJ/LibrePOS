from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from librepos.extensions import db
from librepos.utils import slugify_string

if TYPE_CHECKING:
    from librepos.models.menu_categories import MenuCategory
    from librepos.models.menu_items import MenuItem


class MenuGroup(db.Model):
    """MenuGroup model."""

    __tablename__ = "menu_groups"

    def __init__(self, category_id: int, name: str, **kwargs):
        super(MenuGroup, self).__init__(**kwargs)
        """Create instance."""
        self.category_id = category_id
        self.name = name.capitalize()
        self.slug = slugify_string(name)

    # ForeignKeys
    category_id: Mapped[int] = mapped_column(ForeignKey("menu_categories.id"))

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    slug: Mapped[str] = mapped_column(unique=True)
    active: Mapped[bool] = mapped_column(default=True)

    # Relationships
    # category:Mapped["MenuGroup"] = relationship(back_populates="menu_groups", viewonly=True, order_by="MenuGroup.name")
    category: Mapped["MenuCategory"] = relationship(
        back_populates="menu_groups", order_by="MenuGroup.name"
    )
    menu_items: Mapped[List["MenuItem"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )
