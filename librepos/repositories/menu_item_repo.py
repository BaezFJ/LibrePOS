from librepos.models import MenuItem

from . import EntityRepository


class MenuItemRepository(EntityRepository[MenuItem]):
    def __init__(self):
        super().__init__(MenuItem)

    @staticmethod
    def get_active_items() -> list[MenuItem]:
        return MenuItem.query.filter_by(active=True).all()

    @staticmethod
    def get_items_by_group(group_id: int) -> list[MenuItem]:
        return MenuItem.query.filter_by(group_id=group_id).all()
