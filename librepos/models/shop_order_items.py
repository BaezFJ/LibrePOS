from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from librepos.extensions import db

if TYPE_CHECKING:
    from librepos.models.shop_orders import ShopOrder
    from librepos.models.menu_items import MenuItem


class ShopOrderItem(db.Model):
    """ShopOrderItem model."""

    __tablename__ = "shop_order_items"

    def __init__(self, shop_order_id: int, menu_item_id: int, item_name: str, **kwargs):
        super(ShopOrderItem, self).__init__(**kwargs)
        """Create instance."""
        self.shop_order_id = shop_order_id
        self.menu_item_id = menu_item_id
        self.item_name = item_name.title()

    # ForeignKeys
    shop_order_id: Mapped[int] = mapped_column(ForeignKey("shop_orders.id"))
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
    shop_order: Mapped["ShopOrder"] = relationship(back_populates="items")
    menu_item: Mapped["MenuItem"] = relationship()
