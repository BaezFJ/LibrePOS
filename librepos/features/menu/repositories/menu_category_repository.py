from librepos.common.base_repository import BaseRepository

from ..models import MenuCategory


class MenuCategoryRepository(BaseRepository[MenuCategory]):
    def __init__(self):
        super().__init__(MenuCategory)

    @staticmethod
    def get_active_categories() -> list[MenuCategory]:
        return (
            MenuCategory.query.filter_by(active=True).order_by(MenuCategory.name).all()
        )
