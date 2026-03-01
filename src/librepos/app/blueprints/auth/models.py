"""SQLAlchemy models for auth blueprint."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from librepos.app.extensions import db


# Example model - customize as needed
# class Auth(db.Model):
#     """Model for auth."""
#
#     __tablename__ = "auth"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(100), nullable=False)
#
#     def __repr__(self) -> str:
#         return f"<Auth {self.id}: {self.name}>"
