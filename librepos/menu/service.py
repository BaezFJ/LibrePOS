from .repository import MenuRepository


class MenuService:
    def __init__(self, repo=None):
        self.repo = repo or MenuRepository()

    def create_menu_category(self, data):
        return self.repo.create_category(data)

    def list_menu_categories(self):
        return self.repo.get_all_categories()

    def get_menu_category(self, category_id):
        return self.repo.get_category_by_id(category_id)

    def update_menu_category(self, category_id, data):
        return self.repo.update_category(category_id, data)

    def delete_menu_category(self, category_id):
        return self.repo.delete_category(category_id)

    def list_menu_groups(self):
        return self.repo.get_all_groups()

    def list_menu_items(self):
        return self.repo.get_all_items()
