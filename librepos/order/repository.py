from librepos.extensions import db
from librepos.models.shop_order_items import ShopOrderItem
from librepos.models.shop_orders import ShopOrder
from librepos.models.restaurant import Restaurant


class OrderRepository:
    @staticmethod
    def get_all_orders():
        return ShopOrder.query.order_by().all()

    @staticmethod
    def get_all_orders_by_user_and_status(user_id, status):
        return ShopOrder.query.filter_by(user_id=user_id, status=status).all()

    @staticmethod
    def get_by_id(order_id):
        return ShopOrder.query.get_or_404(order_id)

    @staticmethod
    def create_order(data):
        order = ShopOrder(**data)
        db.session.add(order)
        db.session.commit()
        return order

    def add_item_to_order(self, order_id, item_id, item_name, quantity, price):
        item = ShopOrderItem(
            shop_order_id=order_id,
            menu_item_id=item_id,
            item_name=item_name,
            quantity=quantity,
            price=price,
        )
        db.session.add(item)
        db.session.commit()
        self.update_subtotal(order_id)
        return item

    def remove_item_from_order(self, order_item_id: int):
        item = ShopOrderItem.query.get(order_item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            self.update_subtotal(item.shop_order_id)
            return True
        else:
            return False

    def update_order(self, order_id, data):
        order = self.get_by_id(order_id)
        if not order:
            return None
        for key, value in data.items():
            setattr(order, key, value)
            db.session.commit()
        return order

    def update_subtotal(self, order_id):
        """Update subtotals for a given order."""
        items = ShopOrderItem.query.filter_by(shop_order_id=order_id).all()
        restaurant = Restaurant.query.get(1)
        subtotal = 0
        tax = 0
        tax_percent = (
            restaurant.tax_percentage if restaurant else 825
        )  # 8.25% represented as integer
        for item in items:
            subtotal += item.price * item.quantity
            tax = (
                subtotal * tax_percent
            ) // 10000  # Divide by 10000 to adjust for two percentage conversions
        self.update_order(order_id, {"subtotal_amount": subtotal, "tax_amount": tax})

    def delete_order(self, order_id):
        order = self.get_by_id(order_id)
        if not order:
            return False
        db.session.delete(order)
        db.session.commit()
        return True
