from librepos.common.base_repository import BaseRepository
from ..models import TicketItem


class OrderItemRepository(BaseRepository[TicketItem]):
    def __init__(self):
        super().__init__(TicketItem)

    def add_item_to_order(
            self, order_id: int, item_id: int, item_name: str, quantity: int, price: int
    ):
        """Add an item to an order."""
        item = TicketItem(
            ticket_id=order_id,
            menu_item_id=item_id,
            item_name=item_name,
            quantity=quantity,
            price=price,
        )
        self.add(item)
        return item
