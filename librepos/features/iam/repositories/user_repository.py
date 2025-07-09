from librepos.common.base_repository import BaseRepository

from ..models import User


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    @staticmethod
    def find_by_username(username: str) -> User | None:
        return User.query.filter_by(username=username).first_or_404()
