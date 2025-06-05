from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from librepos.extensions import db


class Restaurant(db.Model):
    """ShopInfo model."""

    __tablename__ = "restaurant"

    def __init__(
            self,
            name: str,
            address: str,
            city: str,
            state: str,
            zipcode: str,
            country: str,
            phone: str,
            email: str,
            **kwargs,
    ):
        super(Restaurant, self).__init__(**kwargs)
        self.name = name.title()
        self.address = address.title()
        self.city = city.title()
        self.state = state.upper()
        self.zipcode = zipcode
        self.country = country.upper()
        self.phone = phone
        self.email = email.lower()

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    address: Mapped[str]
    city: Mapped[str]
    state: Mapped[str]
    zipcode: Mapped[str]
    country: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    website: Mapped[Optional[str]]
    currency: Mapped[str]
    timezone: Mapped[str]
