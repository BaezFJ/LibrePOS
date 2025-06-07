from flask_login import login_user, logout_user

from librepos.utils import FlashMessageHandler
from librepos.repositories.user_repository import UserRepository


class AuthService:

    def __init__(self, repo=None):
        self.repo = repo or UserRepository

    def authenticate(self, email, password, remember):
        user = self.repo.find_by_email(email)
        if not user:
            FlashMessageHandler.error("Invalid email or password.")
            return None
        if not user.active:
            FlashMessageHandler.error("Your account has been deactivated.")
            FlashMessageHandler.info("Please contact the administrator.")
            return None
        if user.check_password(password):
            login_user(user, remember=remember)
            if user.failed_login_count > 0:
                user.reset_failed_login_count()
            FlashMessageHandler.info("Welcome back!")
            return user
        user.handle_failed_login()
        attempts_left = 3 - user.failed_login_count
        if attempts_left > 0:
            _message = f"Invalid password. {attempts_left} attempts remaining."
            FlashMessageHandler.warning(_message)
        else:
            FlashMessageHandler.error("Account locked!.")
        return None

    @staticmethod
    def logout():
        FlashMessageHandler.info("You have been logged out.")
        logout_user()
