from librepos.extensions import db
from librepos.utils import timezone_aware_datetime
from librepos.utils.enums import OrderStateEnum


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
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_number = db.Column(db.Integer, nullable=False)
    status = db.Column(
        db.Enum(OrderStateEnum), nullable=False, default=OrderStateEnum.PENDING
    )
    guest_count = db.Column(db.SmallInteger, nullable=False, default=1)

    subtotal_amount = db.Column(db.Integer, nullable=False, default=0)
    discount_amount = db.Column(db.Integer, nullable=False, default=0)
    tax_amount = db.Column(db.Integer, nullable=False, default=0)
    total_amount = db.Column(db.Integer, nullable=False, default=0)
    paid_amount = db.Column(db.Integer, nullable=False, default=0)
    due_amount = db.Column(db.Integer, nullable=False, default=0)

    created_date = db.Column(db.Date, nullable=False)
    created_time = db.Column(db.Time, nullable=False)
    closed_date = db.Column(db.Date, nullable=True)
    closed_time = db.Column(db.Time, nullable=True)

    # Relationships
    user = db.relationship("User", back_populates="orders")
    items = db.relationship(
        "ShopOrderItem", back_populates="shop_order", cascade="all, delete-orphan"
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
