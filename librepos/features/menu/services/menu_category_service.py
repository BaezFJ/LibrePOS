from flask_login import current_user

from librepos.common.base_service import BaseService
from librepos.features.menu.models import MenuCategory
from librepos.features.menu.repositories import MenuCategoryRepository
from librepos.utils import FlashMessageHandler
from librepos.utils.datetime import timezone_aware_datetime
from librepos.utils.model_utils import update_model_fields
from librepos.utils.validators import validate_exists, validate_confirmation


class MenuCategoryService(BaseService):
    def __init__(self):
        self.repository = MenuCategoryRepository()

    def _validate_category_exists(self, category_id):
        """Validate that a category exists and return it."""
        return validate_exists(self.repository, category_id, "Category not found.")

    def create_category(self, data):
        """Create a new category."""

        new_category = MenuCategory(**data)

        def _create_operation():
            self.repository.add(new_category)
            FlashMessageHandler.success("Category created successfully.")
            return new_category

        return self._execute_with_error_handling(
            _create_operation, "Error creating category"
        )

    def update_category(self, category_id: int, data):
        """Update a category."""

        def _update_operation():
            category = self._validate_category_exists(category_id)
            if not category:
                return None

            # Add update tracking data
            data["updated_by_id"] = current_user.id
            data["updated_at"] = timezone_aware_datetime()

            # Update the fields
            update_model_fields(category, data)

            # Perform the update
            self.repository.update(category)
            FlashMessageHandler.success("Category updated successfully.")
            return category

        return self._execute_with_error_handling(
            _update_operation, "Error updating category"
        )

    def delete_category(self, data, category_id: int):
        """Delete a category."""

        def _delete_operation():
            category = self._validate_category_exists(category_id)
            if not category:
                return None

            # Validate confirmation
            if not validate_confirmation(data):
                return None

            # Perform the deletion
            self.repository.delete(category)
            FlashMessageHandler.success("Category deleted successfully.")
            return True

        return self._execute_with_error_handling(
            _delete_operation, "Error deleting category"
        )
