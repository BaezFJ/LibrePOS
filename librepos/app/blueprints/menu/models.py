"""SQLAlchemy models for menu blueprint."""

from __future__ import annotations

import enum

from sqlalchemy import Column, Enum, ForeignKey, Index, Numeric, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from librepos.app.extensions import db
from librepos.app.shared.mixins import CRUDMixin


class TagType(enum.Enum):
    """Types of tags for menu items."""

    DIETARY = "dietary"
    ALLERGEN = "allergen"
    OTHER = "other"


# Association table for MenuItem <-> Tag many-to-many relationship
menu_item_tags = Table(
    "menu_item_tags",
    db.Model.metadata,
    Column("menu_item_id", ForeignKey("menu_items.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Tag(db.Model, CRUDMixin):
    """Model for reusable menu item tags (dietary info, allergens)."""

    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    type: Mapped[TagType] = mapped_column(Enum(TagType), nullable=False)
    icon: Mapped[str | None] = mapped_column(String(50))

    # Relationship to menu items
    menu_items: Mapped[list[MenuItem]] = relationship(
        secondary=menu_item_tags,
        back_populates="tags",
    )

    __table_args__ = (Index("ix_tags_type", "type"),)

    def __repr__(self) -> str:
        return f"<Tag {self.id}: {self.name} ({self.type.value})>"


class Category(db.Model, CRUDMixin):
    """Model for menu categories."""

    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500))
    image_url: Mapped[str | None] = mapped_column(String(255))
    display_order: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))

    # Self-referential relationship for category hierarchy
    parent: Mapped[Category | None] = relationship(
        back_populates="children",
        remote_side="Category.id",
    )
    children: Mapped[list[Category]] = relationship(
        back_populates="parent",
    )

    # Relationship to menu items
    items: Mapped[list[MenuItem]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
        order_by="MenuItem.display_order",
    )

    def __repr__(self) -> str:
        return f"<Category {self.id}: {self.name}>"


class MenuItem(db.Model, CRUDMixin):
    """Model for menu items."""

    __tablename__ = "menu_items"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500))
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    cost_price: Mapped[float | None] = mapped_column(Numeric(10, 2))
    sku: Mapped[str | None] = mapped_column(String(50), unique=True)
    image_url: Mapped[str | None] = mapped_column(String(255))
    display_order: Mapped[int] = mapped_column(default=0)
    preparation_time: Mapped[int | None] = mapped_column()  # minutes
    tax_rate: Mapped[float] = mapped_column(Numeric(5, 4), default=0)
    is_active: Mapped[bool] = mapped_column(default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    # Relationships
    category: Mapped[Category] = relationship(back_populates="items")
    variants: Mapped[list[MenuItemVariant]] = relationship(
        back_populates="menu_item",
        cascade="all, delete-orphan",
        order_by="MenuItemVariant.display_order",
    )
    tags: Mapped[list[Tag]] = relationship(
        secondary=menu_item_tags,
        back_populates="menu_items",
    )

    __table_args__ = (
        Index("ix_menu_items_category_id", "category_id"),
        Index("ix_menu_items_is_active", "is_active"),
    )

    def __repr__(self) -> str:
        return f"<MenuItem {self.id}: {self.name}>"


class MenuItemVariant(db.Model, CRUDMixin):
    """Model for menu item variants (sizes, options)."""

    __tablename__ = "menu_item_variants"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price_adjustment: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    sku: Mapped[str | None] = mapped_column(String(50), unique=True)
    display_order: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"), nullable=False)

    # Relationship
    menu_item: Mapped[MenuItem] = relationship(back_populates="variants")

    def __repr__(self) -> str:
        return f"<MenuItemVariant {self.id}: {self.name}>"
