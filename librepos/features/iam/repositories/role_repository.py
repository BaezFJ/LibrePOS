from librepos.common.base_repository import BaseRepository

from ..models import Role


class RoleRepository(BaseRepository[Role]):
    def __init__(self):
        super().__init__(Role)

    def get_active_roles(self):
        return self.model_class.query.filter_by(active=True).all()
