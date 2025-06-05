from flask_login import current_user

from librepos.menu.repository import MenuRepository
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

    def add_item_to_order(self, order_id, item_id, quantity, price):
        item = MenuRepository.get_item_by_id(item_id)
        item_name = item.group.name + " - " + item.name if item else ""
        return self.repo.add_item_to_order(
            order_id, item_id, item_name=item_name, quantity=quantity, price=price
        )

    def remove_item_from_order(self, order_item_id):
        return self.repo.remove_item_from_order(order_item_id)

    def update_subtotal(self, order_id):
        return self.repo.update_subtotal(order_id)

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
