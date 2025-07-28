from librepos.common.base_repository import BaseRepository

from ..models import Ticket


class OrderRepository(BaseRepository[Ticket]):
    def __init__(self):
        super().__init__(Ticket)
        self.model_class = Ticket

    def list_orders_by_user(self, user_id):
        return self.model_class.query.filter_by(user_id=user_id).all()
