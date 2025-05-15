from werkzeug.security import check_password_hash
from flask_login import logout_user, login_user, current_user

from librepos.blueprints.users.repositories import UserRepository
from librepos.blueprints.users.models import User


class AuthService:
    def __init__(self, repo=None):
        self.repo = repo or UserRepository()

    def authenticate(self, username: str, password: str) -> User | None:
        user = self.repo.get_by_username(username)
        if user and check_password_hash(user.password, password):
            login_user(user, fresh=True)
            return user
        return None

    @staticmethod
    def logout() -> None:
        logout_user()

    @staticmethod
    def authenticated_user():
        return current_user.is_authenticated
