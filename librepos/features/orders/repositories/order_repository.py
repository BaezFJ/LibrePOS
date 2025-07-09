from librepos.common.base_repository import BaseRepository

from ..models import ShopOrder


class OrderRepository(BaseRepository[ShopOrder]):
    def __init__(self):
        super().__init__(ShopOrder)
        self.model_class = ShopOrder

    def list_orders_by_user(self, user_id):
        return self.model_class.query.filter_by(user_id=user_id).all()
