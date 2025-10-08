from flask_login import current_user

from librepos.common.base_repository import BaseRepository

from ..models import User


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    @staticmethod
    def find_by_username(username: str) -> User | None:
        return User.query.filter_by(username=username).first()

    @staticmethod
    def find_permission(permission_name: str) -> bool:
        if not current_user.role:
            return False
        return current_user.role.has_permission(permission_name)
