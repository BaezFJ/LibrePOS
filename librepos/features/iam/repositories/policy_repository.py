from librepos.common.base_repository import BaseRepository

from ..models import Policy


class PolicyRepository(BaseRepository[Policy]):
    def __init__(self):
        super().__init__(Policy)
