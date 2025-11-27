from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from librepos.utils.datetime import timezone_aware_datetime


class BaseModel(DeclarativeBase):
    """Base model class for all database models."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: timezone_aware_datetime(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=lambda: timezone_aware_datetime(),
        onupdate=lambda: timezone_aware_datetime(),
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}>"
