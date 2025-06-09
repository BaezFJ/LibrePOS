from librepos.models.menu_categories import MenuCategory

from . import EntityRepository


class MenuCategoryRepository(EntityRepository[MenuCategory]):
    def __init__(self):
        super().__init__(MenuCategory)

    @staticmethod
    def get_active_categories() -> list[MenuCategory]:
        return MenuCategory.query.filter_by(active=True).all()
