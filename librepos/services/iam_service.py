from sqlalchemy.exc import SQLAlchemyError

from librepos.repositories import UserRepository, RoleRepository, PolicyRepository
from librepos.utils import FlashMessageHandler
from librepos.utils.model_utils import update_model_fields


class IAMService:
    """Service for Identity and Access Management (IAM) operations."""

    def __init__(self):
        self.user_repository = UserRepository()
        self.role_repository = RoleRepository()
        self.policy_repository = PolicyRepository()

    # ==================================================================================================================
    #                                              USERS
    # ==================================================================================================================

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

    # ==================================================================================================================
    #                                              ROLES
    # ==================================================================================================================

    def create_role(self, data):
        """Create a new role."""
        try:
            role = self.role_repository.model_class(**data)

            self.role_repository.add(role)
            FlashMessageHandler.success("Role created successfully.")
            return role
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error creating role: {str(e)}")
            return None

    def delete_role(self, data, role_id):
        """Delete a role."""
        try:
            role = self.role_repository.get_by_id(role_id)
            confirmation = data.get("confirmation").lower()

            if not role:
                FlashMessageHandler.error("Role not found.")
                return False

            if confirmation != "confirm":
                FlashMessageHandler.error("Invalid confirmation.")
                return False
            self.role_repository.delete(role)
            FlashMessageHandler.success("Role deleted successfully.")
            return True
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error deleting role: {str(e)}")
            return False

    def toggle_role_status(self, role_id):
        """Toggle a role's active status."""
        try:
            role = self.role_repository.get_by_id(role_id)

            if not role:
                FlashMessageHandler.error("Role not found.")
                return False

            role.active = not role.active
            self.role_repository.update(role)
            status = "activated" if role.active else "suspended"
            FlashMessageHandler.success(f"Role {status} successfully.")
            return True
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error toggling role status: {str(e)}")
            return False
