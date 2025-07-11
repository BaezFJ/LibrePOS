from librepos.common.base_service import BaseService
from librepos.features.menu.models import MenuItem
from librepos.features.menu.repositories import MenuItemRepository
from librepos.utils import FlashMessageHandler, convert_dollars_to_cents
from librepos.utils.model_utils import update_model_fields
from librepos.utils.validators import validate_exists


class MenuItemService(BaseService):
    def __init__(self):
        self.repository = MenuItemRepository()

    def _validate_item_exists(self, item_id):
        """Validate that a menu item exists and return it."""
        return validate_exists(self.repository, item_id, "Menu item not found.")

    def create_menu_item(self, data):
        """Create a new menu item."""

        def _create_operation():
            data["price"] = convert_dollars_to_cents(data["price"])
            item = MenuItem(**data)
            self.repository.add(item)
            FlashMessageHandler.success("Menu item created successfully.")
            return item

        return self._execute_with_error_handling(_create_operation, "Error creating menu item")

    def get_item_by_id(self, item_id):
        return self.repository.get_by_id(item_id)

    def list_menu_items(self):
        return self.repository.get_all()

    def list_items_by_group(self, group_id):
        return self.repository.get_items_by_group(group_id)

    def update_menu_item(self, item_id, data):
        """Update a menu item."""

        def _update_operation():
            item = self._validate_item_exists(item_id)
            if not item:
                return None

            # Update the fields
            data["price"] = convert_dollars_to_cents(data["price"])
            update_model_fields(item, data)

            # Perform the update
            self.repository.update(item)
            FlashMessageHandler.success("Menu item updated successfully.")
            return item

        return self._execute_with_error_handling(_update_operation, "Error updating menu item")

    def delete_menu_item(self, item_id):
        """Delete a menu item."""

        def _delete_operation():
            item = self._validate_item_exists(item_id)
            if not item:
                return None

            # Perform the deletion
            self.repository.delete(item)
            FlashMessageHandler.success("Menu item deleted successfully.")
            return True

        return self._execute_with_error_handling(_delete_operation, "Error deleting menu item")
