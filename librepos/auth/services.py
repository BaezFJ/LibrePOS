from werkzeug.security import check_password_hash

from .repositories import UserRepository
from .models import User


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def authenticate(self, username: str, password: str) -> User | None:
        user = self._user_repo.get_by_username(username)
        if user and check_password_hash(user.password, password):
            return user
        return None
