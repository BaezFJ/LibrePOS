from flask_login import current_user

from librepos.models.shop_orders import OrderStateEnum

from .repository import OrderRepository


class OrderService:
    def __init__(self, repo=None):
        self.repo = repo or OrderRepository()

    def create_order(self):
        data = {
            "user_id": current_user.id,
        }
        return self.repo.create_order(data)

    def list_orders(self):
        return self.repo.get_all_orders()

    def list_user_pending_orders(self):
        return self.repo.get_all_orders_by_user_and_status(
            user_id=current_user.id, status=OrderStateEnum.PENDING.value
        )

    def get_order(self, order_id):
        return self.repo.get_by_id(order_id)

    def mark_order_as_voided(self, order_id):
        data = {
            "status": OrderStateEnum.VOIDED.value,
        }
        return self.repo.update_order(order_id, data)
