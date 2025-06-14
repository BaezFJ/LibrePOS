from librepos.models import Role

from . import EntityRepository


class RoleRepository(EntityRepository[Role]):
    def __init__(self):
        super().__init__(Role)
