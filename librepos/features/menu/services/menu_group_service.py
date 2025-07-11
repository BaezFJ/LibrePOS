from librepos.common.base_service import BaseService
from librepos.features.menu.repositories import MenuGroupRepository
from librepos.utils import FlashMessageHandler
from librepos.utils.model_utils import update_model_fields
from librepos.utils.validators import validate_exists


class MenuGroupService(BaseService):
    def __init__(self):
        self.repository = MenuGroupRepository()

    def _validate_group_exists(self, group_id):
        """Validate that a group exists and return it."""
        return validate_exists(self.repository, group_id, "Group not found.")

    def create_group(self, data):
        """Create a new group."""

        new_group = self.repository.model_class(**data)

        def _create_operation():
            self.repository.add(new_group)
            FlashMessageHandler.success("Group created successfully.")
            return new_group

        return self._execute_with_error_handling(_create_operation, "Error creating group")

    def update_group(self, group_id: int, data):
        """Update a group."""

        def _update_operation():
            group = self._validate_group_exists(group_id)
            if not group:
                return None

            # Update the fields
            update_model_fields(group, data)

            # Perform the update
            self.repository.update(group)
            FlashMessageHandler.success("Group updated successfully.")
            return group

        return self._execute_with_error_handling(_update_operation, "Error updating group")

    def delete_group(self, group_id):
        """Delete a group."""

        def _delete_operation():
            group = self._validate_group_exists(group_id)
            if not group:
                return None

            # Perform the deletion
            self.repository.delete(group)
            FlashMessageHandler.success("Group deleted successfully.")
            return True

        return self._execute_with_error_handling(_delete_operation, "Error deleting group")
