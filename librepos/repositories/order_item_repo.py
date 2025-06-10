from librepos.models.shop_order_items import ShopOrderItem

from . import EntityRepository


class OrderItemRepository(EntityRepository[ShopOrderItem]):
    def __init__(self):
        super().__init__(ShopOrderItem)

    def add_item_to_order(
        self, order_id: int, item_id: int, item_name: str, quantity: int, price: int
    ):
        """Add an item to an order."""
        item = ShopOrderItem(
            shop_order_id=order_id,
            menu_item_id=item_id,
            item_name=item_name,
            quantity=quantity,
            price=price,
        )
        self.add(item)
        return item
