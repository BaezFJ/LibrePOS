from sqlalchemy.exc import SQLAlchemyError

from librepos.repositories import OrderItemRepository, MenuItemRepository
from librepos.utils import FlashMessageHandler


class OrderItemService:
    def __init__(self):
        self.repository = OrderItemRepository()

    def add_item_to_order(self, order_id: int, item_id: int, quantity: int, price: int):
        """Add an item to an order."""
        item = MenuItemRepository().get_by_id(item_id)
        item_name = item.group.name + " - " + item.name if item else "N/A"
        return self.repository.add_item_to_order(
            order_id, item_id, item_name, quantity, price
        )

    def remove_item_from_order(self, order_item_id: int):
        """Remove an item from an order."""
        try:
            order_item = self.repository.get_by_id(order_item_id)

            if not order_item:
                FlashMessageHandler.error("Order item not found.")
                return None, False

            self.repository.delete(order_item)
            FlashMessageHandler.success("Order item removed successfully.")
            return order_item, True

        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error removing order item: {str(e)}")
            return None, False
