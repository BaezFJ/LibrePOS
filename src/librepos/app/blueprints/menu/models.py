"""SQLAlchemy models for menu blueprint."""

from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from librepos.app.extensions import db
from librepos.app.shared.mixins import CRUDMixin


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

    def __repr__(self) -> str:
        return f"<Category {self.id}: {self.name}>"
