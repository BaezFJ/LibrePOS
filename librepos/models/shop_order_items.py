from librepos.extensions import db


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
    shop_order_id = db.Column(db.Integer, db.ForeignKey("shop_orders.id"))
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"))

    # Columns
    id = db.Column(db.Integer, primary_key=True)

    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(
        db.Integer, nullable=False, default=0
    )  # price per unit at time of sale
    total = db.Column(db.Integer, nullable=False, default=0)  # quantity * price
    item_name = db.Column(
        db.String(255), nullable=False
    )  # store item-name in case the menu changes later

    # Relationships
    shop_order = db.relationship("ShopOrder", back_populates="items")
    menu_item = db.relationship("MenuItem")
