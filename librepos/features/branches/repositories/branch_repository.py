from librepos.common.base_repository import BaseRepository
from ..models import Branch


class BranchRepository(BaseRepository[Branch]):
    def __init__(self):
        super().__init__(Branch)
