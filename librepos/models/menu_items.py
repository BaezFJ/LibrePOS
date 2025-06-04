from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from librepos.extensions import db
from librepos.utils import slugify_string

if TYPE_CHECKING:
    from librepos.models.menu_groups import MenuGroup


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
        self.slug = slugify_string(name)
        self.description = description.capitalize()
        self.price = price

    # ForeignKeys
    group_id: Mapped[int] = mapped_column(ForeignKey("menu_groups.id"))

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    slug: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    price: Mapped[int] = mapped_column(default=0)
    active: Mapped[bool] = mapped_column(default=True)

    # Relationships
    group: Mapped["MenuGroup"] = relationship(back_populates="menu_items")

    @property
    def item_name_with_group(self):
        return f"{self.group.name} - {self.name}"
