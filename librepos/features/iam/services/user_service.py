from librepos.common.base_service import BaseService
from librepos.features.iam.repositories import UserRepository
from librepos.utils import FlashMessageHandler
from librepos.utils.model_utils import update_model_fields
from librepos.utils.validators import validate_exists, validate_confirmation


class UserService(BaseService):
    def __init__(self):
        self.user_repository = UserRepository()

    def _validate_user_exists(self, user_id):
        """Validate that a user exists and return it."""
        return validate_exists(self.user_repository, user_id, "User not found.")

    def create_user(self, data):
        """Create a new user."""

        def _create_operation():
            user = self.user_repository.model_class(**data)
            self.user_repository.add(user)
            return user

        return self._execute_with_error_handling(
            _create_operation, "Error creating user"
        )

    def delete_user(self, data):
        """Delete a user."""

        def _delete_operation():
            user = self._validate_user_exists(data.get("id"))
            if not user:
                return False

            if not validate_confirmation(data):
                return False

            self.user_repository.delete(user)
            return True

        return self._execute_with_error_handling(
            _delete_operation, "Error deleting user"
        )

    def toggle_user_status(self, user_id):
        """Toggle a user's active status."""

        def _toggle_operation():
            user = self._validate_user_exists(user_id)
            if not user:
                return False

            user.active = not user.active
            self.user_repository.update(user)
            status = "activated" if user.active else "suspended"
            FlashMessageHandler.success(f"User {status} successfully.")
            return True

        return self._execute_with_error_handling(
            _toggle_operation, "Error toggling user status"
        )

    def update_user(self, user_id, data):
        """Update a user."""

        def _update_operation():
            user = self._validate_user_exists(user_id)
            if not user:
                return False

            update_model_fields(user, data)
            self.user_repository.update(user)
            FlashMessageHandler.success("User updated successfully.")
            return True

        return self._execute_with_error_handling(
            _update_operation, "Error updating user"
        )
