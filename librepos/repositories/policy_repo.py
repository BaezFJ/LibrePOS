from librepos.models import Policy

from . import EntityRepository


class PolicyRepository(EntityRepository[Policy]):
    def __init__(self):
        super().__init__(Policy)

    @staticmethod
    def list_active_policies():
        return Policy.query.filter(Policy.active).all()
