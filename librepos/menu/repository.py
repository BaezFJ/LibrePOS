from librepos.extensions import db

from librepos.models.menu_categories import MenuCategory
from librepos.models.menu_groups import MenuGroup
from librepos.models.menu_items import MenuItem


class MenuRepository:
    @staticmethod
    def create_category(data):
        category = MenuCategory(**data)
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def get_all_categories():
        return MenuCategory.query.order_by(MenuCategory.name).all()

    @staticmethod
    def get_category_by_id(category_id):
        return MenuCategory.query.get(category_id)

    def update_category(self, category_id, data):
        category = self.get_category_by_id(category_id)
        if not category:
            return None
        for key, value in data.items():
            setattr(category, key, value)
        db.session.commit()
        return category

    def delete_category(self, category_id):
        category = self.get_category_by_id(category_id)
        if not category:
            return False
        db.session.delete(category)
        db.session.commit()
        return True

    @staticmethod
    def get_all_groups():
        return MenuGroup.query.order_by(MenuGroup.name).all()

    @staticmethod
    def get_all_items():
        return MenuItem.query.order_by(MenuItem.name).all()
