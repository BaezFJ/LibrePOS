from librepos.models import Role

from . import EntityRepository


class RoleRepository(EntityRepository[Role]):
    def __init__(self):
        super().__init__(Role)

    def get_active_roles(self):
        return self.model_class.query.filter_by(active=True).all()
