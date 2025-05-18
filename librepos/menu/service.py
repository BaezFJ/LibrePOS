from .repository import MenuRepository


class MenuService:
    def __init__(self, repo=None):
        self.repo = repo or MenuRepository()

    # ======================================================
    #                   MENU - CATEGORY
    # ======================================================

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

    # ======================================================
    #                   MENU - GROUP
    # ======================================================

    def create_menu_group(self, data):
        return self.repo.create_group(data)

    def list_menu_groups(self):
        return self.repo.get_all_groups()

    def get_menu_group(self, group_id):
        return self.repo.get_group_by_id(group_id)

    def update_menu_group(self, group_id, data):
        return self.repo.update_group(group_id, data)

    def delete_menu_group(self, group_id):
        return self.repo.delete_group(group_id)

    # ======================================================
    #                   MENU - ITEM
    # ======================================================

    def list_menu_items(self):
        return self.repo.get_all_items()
