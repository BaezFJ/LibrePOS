from librepos.extensions import db
from librepos.models.shop_orders import ShopOrder
from librepos.models.shop_order_items import ShopOrderItem


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

    @staticmethod
    def add_item_to_order(order_id, item_id, item_name):
        item = ShopOrderItem(
            shop_order_id=order_id, menu_item_id=item_id, item_name=item_name
        )
        db.session.add(item)
        db.session.commit()
        return item

    def update_order(self, order_id, data):
        order = self.get_by_id(order_id)
        if not order:
            return None
        for key, value in data.items():
            setattr(order, key, value)
            db.session.commit()
        return order

    def delete_order(self, order_id):
        order = self.get_by_id(order_id)
        if not order:
            return False
        db.session.delete(order)
        db.session.commit()
        return True
