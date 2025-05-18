from .repository import MenuRepository


class MenuService:
    def __init__(self, repo=None):
        self.repo = repo or MenuRepository()

    def list_menu_categories(self):
        return self.repo.get_all_categories()

    def list_menu_groups(self):
        return self.repo.get_all_groups()

    def list_menu_items(self):
        return self.repo.get_all_items()
