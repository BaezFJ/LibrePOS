from librepos.common.base_service import BaseService
from librepos.utils import FlashMessageHandler
from librepos.utils.model_utils import update_model_fields
from librepos.utils.validators import validate_exists

from ..repositories import BranchRepository


class BranchService(BaseService):
    def __init__(self):
        self.repository = BranchRepository()

    def get_restaurant_by_id(self, restaurant_id):
        return self.repository.get_by_id(restaurant_id)

    def update_restaurant(self, data):
        """Update restaurant details."""

        def _update_operation():
            branch = validate_exists(
                self.repository, data.get("id"), "Restaurant not found."
            )
            if not branch:
                return None

            update_model_fields(branch, data)
            self.repository.update(branch)
            FlashMessageHandler.success("Restaurant updated successfully.")
            return branch

        return self._execute_with_error_handling(
            _update_operation, "Error updating restaurant"
        )
