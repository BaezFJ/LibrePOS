from librepos.users.repositories import UserRepository
from werkzeug.security import check_password_hash
from flask_login import login_user


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def authenticate(self, username: str, password: str):
        user = self._user_repo.get_by_username(username)
        if not user or not check_password_hash(user.password, password):
            raise ValueError("Invalid credentials please try again.")
        if not user.is_active:
            raise ValueError("User is not active")
        login_user(user, fresh=True)
        return user
