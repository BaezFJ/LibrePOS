from librepos.common.base_service import BaseService
from librepos.utils import FlashMessageHandler
from librepos.utils.validators import validate_exists, validate_confirmation
from ..repositories import RoleRepository


class RoleService(BaseService):
    def __init__(self):
        self.role_repository = RoleRepository()

    def _validate_role_exists(self, role_id):
        """Validate that a role exists and return it."""
        return validate_exists(self.role_repository, role_id, "Role not found.")

    def create_role(self, data):
        """Create a new role."""

        def _create_operation():
            role = self.role_repository.model_class(**data)
            self.role_repository.add(role)
            FlashMessageHandler.success("Role created successfully.")
            return role

        return self._execute_with_error_handling(
            _create_operation, "Error creating role"
        )

    def delete_role(self, data, role_id):
        """Delete a role."""

        def _delete_operation():
            role = self._validate_role_exists(role_id)
            if not role:
                return False

            if not validate_confirmation(data):
                return False

            self.role_repository.delete(role)
            FlashMessageHandler.success("Role deleted successfully.")
            return True

        return self._execute_with_error_handling(
            _delete_operation, "Error deleting role"
        )

    def toggle_role_status(self, role_id):
        """Toggle a role's active status."""

        def _toggle_operation():
            role = self._validate_role_exists(role_id)
            if not role:
                return False

            role.active = not role.active
            self.role_repository.update(role)
            status = "activated" if role.active else "suspended"
            FlashMessageHandler.success(f"Role {status} successfully.")
            return True

        return self._execute_with_error_handling(
            _toggle_operation, "Error toggling role status"
        )
