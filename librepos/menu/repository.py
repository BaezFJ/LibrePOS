from librepos.models.menu_categories import MenuCategory
from librepos.models.menu_groups import MenuGroup
from librepos.models.menu_items import MenuItem


class MenuRepository:
    @staticmethod
    def get_all_categories():
        return MenuCategory.query.order_by(MenuCategory.name).all()

    @staticmethod
    def get_all_groups():
        return MenuGroup.query.order_by(MenuGroup.name).all()

    @staticmethod
    def get_all_items():
        return MenuItem.query.order_by(MenuItem.name).all()
