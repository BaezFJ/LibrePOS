from sqlalchemy.exc import SQLAlchemyError

from librepos.repositories import UserRepository
from librepos.utils.model_utils import update_model_fields
from librepos.utils import FlashMessageHandler


class UserService:
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()

    def list_users(self):
        return self.user_repository.get_all()

    def get_user(self, user_id):
        return self.user_repository.get_by_id(user_id)

    def create_user(self, data):
        return self.user_repository.add(data)

    def update_user(self, user_id: int, data):
        try:
            # Get the existing user
            user = self.user_repository.get_by_id(user_id)
            if not user:
                FlashMessageHandler.error("User not found.")
                return None, False

            # Update the fields
            update_model_fields(user, data)

            # Perform the update
            updated_user = self.user_repository.update(user)
            FlashMessageHandler.success("User updated successfully.")
            return updated_user, True

        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error updating user: {str(e)}")
            return None, False
