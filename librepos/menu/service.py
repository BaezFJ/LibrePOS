from librepos.utils import convert_dollars_to_cents

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

    def list_active_menu_categories(self):
        return self.repo.get_all_categories()

    def get_menu_category(self, category_id):
        return self.repo.get_category_by_id(category_id)

    def get_active_menu_categories(self):
        return self.repo.get_active_categories()

    def get_menu_category_groups(self, category_id):
        return self.repo.get_category_groups(category_id)

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

    def create_menu_item(self, data):
        menu_group = self.get_menu_group(data["group_id"])
        item_name = data["name"]
        data["price"] = convert_dollars_to_cents(data["price"])
        if menu_group and item_name:
            data["name"] = f"{menu_group.name} - {item_name}"
        return self.repo.create_item(data)

    def list_menu_items(self):
        return self.repo.get_all_items()

    def list_group_menu_items(self, group_id):
        return self.repo.get_all_items_by_group(group_id)

    def get_menu_item(self, item_id):
        return self.repo.get_item_by_id(item_id)

    def update_menu_item(self, item_id, data):
        data["price"] = convert_dollars_to_cents(data["price"])
        return self.repo.update_item(item_id, data)

    def delete_menu_item(self, item_id):
        return self.repo.delete_item(item_id)
