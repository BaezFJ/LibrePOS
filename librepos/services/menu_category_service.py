from sqlalchemy.exc import SQLAlchemyError

from librepos.repositories import MenuCategoryRepository
from librepos.models.menu_categories import MenuCategory
from librepos.utils.model_utils import update_model_fields
from librepos.utils import FlashMessageHandler


class MenuCategoryService:
    def __init__(self):
        self.repository = MenuCategoryRepository()

    def create_category(self, data):
        category = MenuCategory(**data)
        self.repository.add(category)

    def list_categories(self):
        return self.repository.get_all()

    def list_active_categories(self):
        return self.repository.get_active_categories()

    def get_category_by_id(self, category_id):
        return self.repository.get_by_id(category_id)

    def update_category(self, category_id: int, data):
        try:
            # Get the existing category
            category = self.get_category_by_id(category_id)

            if not category:
                FlashMessageHandler.error("Category not found.")
                return None, False

            # Update the fields
            update_model_fields(category, data)

            # Perform the update
            self.repository.update(category)
            FlashMessageHandler.success("Category updated successfully.")
            return category, True
        except SQLAlchemyError as e:
            FlashMessageHandler.error(f"Error updating category: {str(e)}")
            return None, False

    def delete_category(self, category_id):
        category = self.get_category_by_id(category_id)
        if not category:
            FlashMessageHandler.error("Category not found.")
            return None, False
        self.repository.delete(category)
        return True
