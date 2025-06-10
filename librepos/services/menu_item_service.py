from sqlalchemy.exc import SQLAlchemyError

from librepos.models.menu_items import MenuItem
from librepos.repositories import MenuItemRepository
from librepos.utils import FlashMessageHandler, convert_dollars_to_cents
from librepos.utils.model_utils import update_model_fields


class MenuItemService:
    def __init__(self):
        self.repository = MenuItemRepository()

    def create_menu_item(self, data):
        data["price"] = convert_dollars_to_cents(data["price"])
        item = MenuItem(**data)
        try:
            self.repository.add(item)
            FlashMessageHandler.success("Menu item created successfully.")
            return item
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error creating menu item: {str(e)}")
            return None

    def get_item_by_id(self, item_id):
        return self.repository.get_by_id(item_id)

    def list_menu_items(self):
        return self.repository.get_all()

    def list_items_by_group(self, group_id):
        return self.repository.get_items_by_group(group_id)

    def update_menu_item(self, item_id, data):
        try:
            # Get existing item
            item = self.get_item_by_id(item_id)

            if not item:
                FlashMessageHandler.error("Menu item not found.")
                return None, False

            # Update the fields
            data["price"] = convert_dollars_to_cents(data["price"])
            update_model_fields(item, data)

            # Perform the update
            self.repository.update(item)
            FlashMessageHandler.success("Menu item updated successfully.")
            return item, True
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error updating menu item: {str(e)}")
            return None, False

    def delete_menu_item(self, item_id):
        item = self.get_item_by_id(item_id)
        if not item:
            FlashMessageHandler.error("Menu item not found.")
            return None, False
        self.repository.delete(item)
        FlashMessageHandler.success("Menu item deleted successfully.")
        return True
