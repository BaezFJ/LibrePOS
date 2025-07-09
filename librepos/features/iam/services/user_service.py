from sqlalchemy.exc import SQLAlchemyError

from librepos.features.iam.repositories import UserRepository
from librepos.utils import FlashMessageHandler
from librepos.utils.model_utils import update_model_fields


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def create_user(self, data):
        """Create a new user."""
        try:
            user = self.user_repository.model_class(**data)

            self.user_repository.add(user)
            FlashMessageHandler.success("User created successfully.")
            return user

        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error creating user: {str(e)}")
            return None

    def delete_user(self, data):
        """Delete a user."""
        try:
            user = self.user_repository.get_by_id(data.get("id"))
            confirmation = data.get("confirmation").lower()

            if not user:
                FlashMessageHandler.error("User not found.")
                return False

            if confirmation != "confirm":
                FlashMessageHandler.error("Invalid confirmation.")
                return False

            self.user_repository.delete(user)
            FlashMessageHandler.success("User deleted successfully.")
            return True
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error deleting user: {str(e)}")
            return False

    def toggle_user_status(self, user_id):
        """Toggle a user's active status."""
        try:
            user = self.user_repository.get_by_id(user_id)

            if not user:
                FlashMessageHandler.error("User not found.")
                return False

            user.active = not user.active
            self.user_repository.update(user)
            status = "activated" if user.active else "suspended"
            FlashMessageHandler.success(f"User {status} successfully.")
            return True
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error toggling user status: {str(e)}")
            return False

    def update_user(self, user_id, data):
        """Update a user."""
        try:
            user = self.user_repository.get_by_id(user_id)

            if not user:
                FlashMessageHandler.error("User not found.")
                return False

            update_model_fields(user, data)
            self.user_repository.update(user)
            FlashMessageHandler.success("User updated successfully.")
            return True
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error updating user: {str(e)}")
