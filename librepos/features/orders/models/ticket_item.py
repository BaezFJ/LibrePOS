from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from librepos.extensions import db

if TYPE_CHECKING:
    from librepos.features.orders.models import Ticket
    from librepos.features.menu.models import MenuItem


class TicketItem(db.Model):
    """TicketItem model."""

    __tablename__ = "ticket_items"

    def __init__(self, ticket_id: int, menu_item_id: int, item_name: str, **kwargs):
        super(TicketItem, self).__init__(**kwargs)
        """Create instance."""
        self.ticket_id = ticket_id
        self.menu_item_id = menu_item_id
        self.item_name = item_name.title()

    # ForeignKeys
    ticket_id: Mapped[int] = mapped_column(ForeignKey("ticket.id"))
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"))

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(default=1)
    price: Mapped[int] = mapped_column(default=0)  # price per unit at time of sale
    total: Mapped[int] = mapped_column(default=0)  # quantity * price
    item_name: Mapped[str]  # store item-name in case the menu changes later
    voided: Mapped[bool] = mapped_column(
        default=False
    )  # manager removed item after completion
    completed: Mapped[bool] = mapped_column(
        default=False
    )  # the kitchen is done preparing
    send_to_prep: Mapped[bool] = mapped_column(
        default=False
    )  # item was sent to the kitchen / bar

    # Relationships
    ticket: Mapped["Ticket"] = relationship(back_populates="items")
    menu_item: Mapped["MenuItem"] = relationship()
