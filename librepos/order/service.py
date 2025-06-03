from flask_login import current_user

from librepos.models.shop_orders import OrderStateEnum
from librepos.menu.repository import MenuRepository

from .repository import OrderRepository


class OrderService:
    def __init__(self, repo=None):
        self.repo = repo or OrderRepository()

    def create_order(self):
        data = {
            "user_id": current_user.id,
        }
        return self.repo.create_order(data)

    def add_item_to_order(self, order_id, item_id):
        item = MenuRepository.get_item_by_id(item_id)
        item_name = item.item_name_with_group if item else ""
        return self.repo.add_item_to_order(order_id, item_id, item_name=item_name)

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
