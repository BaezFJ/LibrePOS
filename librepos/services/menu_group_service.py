from sqlalchemy.exc import SQLAlchemyError

from librepos.models.menu_groups import MenuGroup
from librepos.repositories import MenuGroupRepository
from librepos.utils.model_utils import update_model_fields
from librepos.utils import FlashMessageHandler


class MenuGroupService:
    def __init__(self):
        self.repository = MenuGroupRepository()

    def create_group(self, data):
        group = MenuGroup(**data)
        try:
            self.repository.add(group)
            FlashMessageHandler.success("Group created successfully.")
            return group
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error creating group: {str(e)}")
            return None

    def get_group_by_id(self, group_id):
        return self.repository.get_by_id(group_id)

    def list_groups(self):
        return self.repository.get_all()

    def list_active_groups(self):
        return self.repository.get_active_groups()

    def list_groups_by_category(self, category_id: int):
        return self.repository.list_groups_by_category(category_id)

    def update_group(self, group_id: int, data):
        try:
            # Get the existing group
            group = self.get_group_by_id(group_id)

            if not group:
                FlashMessageHandler.error("Group not found.")
                return None, False

            # Update the fields
            update_model_fields(group, data)

            # Perform the update
            self.repository.update(group)
            FlashMessageHandler.success("Group updated successfully.")
            return group, True
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error updating group: {str(e)}")
            return None, False

    def delete_group(self, group_id):
        group = self.get_group_by_id(group_id)
        if not group:
            FlashMessageHandler.error("Group not found.")
            return None, False
        self.repository.delete(group)
        FlashMessageHandler.success("Group deleted successfully.")
        return True
