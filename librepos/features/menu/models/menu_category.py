from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from librepos.extensions import db
from librepos.utils import slugify_string

if TYPE_CHECKING:
    from .menu_group import MenuGroup


class MenuCategory(db.Model):
    """MenuCategory model."""

    __tablename__ = "menu_categories"

    def __init__(self, name: str, **kwargs):
        super(MenuCategory, self).__init__(**kwargs)
        self.name = name.capitalize()
        self.slug = slugify_string(name)

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    slug: Mapped[str] = mapped_column(unique=True)
    active: Mapped[bool] = mapped_column(default=True)

    # Relationships
    menu_groups: Mapped[List["MenuGroup"]] = relationship(back_populates="category")
