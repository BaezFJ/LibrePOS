from datetime import date, time
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, relationship, mapped_column

from librepos.extensions import db
from librepos.utils import timezone_aware_datetime
from librepos.utils.enums import OrderStateEnum

if TYPE_CHECKING:
    from librepos.features.orders.models import ShopOrderItem
    from librepos.features.iam.models import User


class ShopOrder(db.Model):
    """ShopOrder model."""

    __tablename__ = "shop_orders"

    def __init__(self, user_id: int, **kwargs):
        super(ShopOrder, self).__init__(**kwargs)
        self.user_id = user_id
        self.order_number = self.get_next_order_number()
        self.created_date = timezone_aware_datetime().date()
        self.created_time = timezone_aware_datetime().time()

    # ForeignKeys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_number: Mapped[int]
    status: Mapped[OrderStateEnum] = mapped_column(
        Enum(OrderStateEnum), default=OrderStateEnum.PENDING
    )
    guest_count: Mapped[int] = mapped_column(default=1)

    subtotal_amount: Mapped[int] = mapped_column(default=0)
    discount_amount: Mapped[int] = mapped_column(default=0)
    tax_amount: Mapped[int] = mapped_column(default=0)
    total_amount: Mapped[int] = mapped_column(default=0)
    paid_amount: Mapped[int] = mapped_column(default=0)
    due_amount: Mapped[int] = mapped_column(default=0)

    created_date: Mapped[date]
    created_time: Mapped[time]
    closed_date: Mapped[Optional[date]]
    closed_time: Mapped[Optional[time]]

    # Relationships
    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[List["ShopOrderItem"]] = relationship(
        back_populates="shop_order", cascade="all, delete-orphan"
    )

    # payment = db.relationship("ShopOrderPayment", back_populates="shop_order")

    @staticmethod
    def get_next_order_number():
        today = timezone_aware_datetime().date()
        daily_orders = ShopOrder.query.filter_by(created_date=today).all()
        if daily_orders:
            return daily_orders[-1].order_number + 1
        else:
            return 1
