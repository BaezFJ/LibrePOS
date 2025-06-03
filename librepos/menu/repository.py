from librepos.extensions import db

from librepos.models.menu_categories import MenuCategory
from librepos.models.menu_groups import MenuGroup
from librepos.models.menu_items import MenuItem


class MenuRepository:
    # ======================================================
    #                   MENU - CATEGORY
    # ======================================================
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
    def get_active_categories():
        return (
            MenuCategory.query.filter_by(active=True).order_by(MenuCategory.name).all()
        )

    @staticmethod
    def get_category_groups(category_id):
        return (
            MenuGroup.query.filter_by(category_id=category_id)
            .order_by(MenuGroup.name)
            .all()
        )

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

    # ======================================================
    #                   MENU - GROUP
    # ======================================================

    @staticmethod
    def create_group(data):
        group = MenuGroup(**data)
        db.session.add(group)
        db.session.commit()
        return group

    @staticmethod
    def get_all_groups():
        return MenuGroup.query.order_by(MenuGroup.name).all()

    @staticmethod
    def get_group_by_id(group_id):
        return MenuGroup.query.get(group_id)

    def update_group(self, group_id, data):
        group = self.get_group_by_id(group_id)
        if not group:
            return None
        for key, value in data.items():
            setattr(group, key, value)
        db.session.commit()
        return group

    def delete_group(self, group_id):
        group = self.get_group_by_id(group_id)
        if not group:
            return False
        db.session.delete(group)
        db.session.commit()
        return True

    # ======================================================
    #                   MENU - ITEM
    # ======================================================
    @staticmethod
    def create_item(data):
        item = MenuItem(**data)
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def get_all_items():
        return MenuItem.query.order_by(MenuItem.name).all()

    @staticmethod
    def get_all_items_by_group(group_id):
        return MenuItem.query.filter_by(group_id=group_id).order_by(MenuItem.name).all()

    @staticmethod
    def get_item_by_id(item_id):
        return MenuItem.query.get(item_id)

    def update_item(self, item_id, data):
        item = self.get_item_by_id(item_id)
        if not item:
            return None
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        return item

    def delete_item(self, item_id):
        item = self.get_item_by_id(item_id)
        if not item:
            return False
        db.session.delete(item)
        db.session.commit()
        return True
