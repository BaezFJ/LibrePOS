from librepos.utils import FlashMessageHandler
from librepos.utils.model_utils import update_model_fields

from ..repositories import BranchRepository


class BranchService:
    def __init__(self):
        self.repository = BranchRepository()

    def get_restaurant_by_id(self, restaurant_id):
        return self.repository.get_by_id(restaurant_id)

    def update_restaurant(self, data):
        """Update restaurant details."""

        try:
            restaurant = self.repository.get_by_id(1)

            if not restaurant:
                FlashMessageHandler.error("Restaurant not found.")
                return None, False

            update_model_fields(restaurant, data)
            self.repository.update(restaurant)
            FlashMessageHandler.success("Restaurant updated successfully.")
            return restaurant, True
        except Exception as e:
            FlashMessageHandler.error(f"Error updating restaurant: {str(e)}")
            return None, False
