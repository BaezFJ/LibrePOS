from typing import Any

from sqlalchemy.exc import SQLAlchemyError

from librepos.utils import FlashMessageHandler
from librepos.utils.enums import OrderStateEnum
from ..repositories import OrderRepository, OrderItemRepository


class OrderService:
    def __init__(self):
        self.order_repo = OrderRepository()
        self.order_item_repo = OrderItemRepository()

    def create_order(self, data: dict[str, Any]):
        order = self.order_repo.model_class(**data)
        return self.order_repo.add(order)

    def list_user_pending_orders(self, user_id: int):
        user_orders = self.order_repo.list_orders_by_user(user_id)
        user_pending_orders = []
        for order in user_orders:
            if order.status == OrderStateEnum.PENDING.value:
                user_pending_orders.append(order)
        return user_pending_orders

    def patch_order_status(self, order_id: int, status: OrderStateEnum):
        try:
            # Get the existing order
            order = self.order_repo.get_by_id(order_id)

            if not order:
                FlashMessageHandler.error("Order not found.")
                return None, False

            # Update the status field
            order.status = status

            # Perform the update
            self.order_repo.update(order)
            FlashMessageHandler.success("Order status updated successfully.")
            return order, True
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error updating order status: {str(e)}")
            return None, False

    def update_order_subtotals(self, order_id):
        """Update subtotals for a given order."""
        try:
            order = self.order_repo.get_by_id(order_id)

            if not order:
                FlashMessageHandler.error("Order not found.")
                return None, False

            subtotal = 0
            tax = 0
            tax_percentage = 825

            for item in order.items:
                subtotal += item.price * item.quantity
                tax = (subtotal * tax_percentage) // 10000

            order.subtotal_amount = subtotal
            order.tax_amount = tax
            order.total_amount = subtotal + tax
            self.order_repo.update(order)
            return order, True

        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error updating order: {str(e)}")
            return None, False

    def remove_item_from_order(self, item_id: int):
        pass
