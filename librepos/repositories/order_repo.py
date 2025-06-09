from librepos.models.shop_orders import ShopOrder

from . import EntityRepository


class OrderRepository(EntityRepository[ShopOrder]):
    def __init__(self):
        super().__init__(ShopOrder)
        self.model_class = ShopOrder

    def list_orders_by_user(self, user_id):
        return self.model_class.query.filter_by(user_id=user_id).all()
