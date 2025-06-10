from librepos.models.restaurant import Restaurant

from . import EntityRepository


class RestaurantRepository(EntityRepository[Restaurant]):
    def __init__(self):
        super().__init__(Restaurant)
