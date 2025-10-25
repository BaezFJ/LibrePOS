from urllib.parse import urlparse

from flask import redirect, url_for, request
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from librepos.features.iam.repositories import IAMUserRepository
from librepos.utils import FlashMessageHandler


class AuthenticationService:
    MAX_LOGIN_ATTEMPTS = 3

    def __init__(self, repo=None):
        self.auth_user_repo = repo or IAMUserRepository()
        self.dashboard_url = "core.home"

    @staticmethod
    def verify_password(user, password: str) -> bool:
        if not user or not user.password:
            return False
        return check_password_hash(user.password, password)

    @staticmethod
    def _is_url_safe(url: str) -> bool:
        """Check if the URL is safe for redirection (no external domains)."""
        if not url:
            return True

        parsed_url = urlparse(url)

        # Reject URLs with scheme or netloc (external URLs)
        if parsed_url.scheme or parsed_url.netloc:
            return False

        # Reject URLs starting with // (protocol-relative URLs)
        if url.startswith("//"):
            return False

        return True

    def handle_next_url(self):
        next_url = request.args.get("next", "")
        next_url = next_url.replace("\\", "")  # Normalize backslashes

        if self._is_url_safe(next_url):
            return redirect(next_url or url_for(self.dashboard_url))

        return redirect(url_for(self.dashboard_url))

    def reset_failed_login_count(self, user) -> None:
        user.failed_login_count = 0
        self.auth_user_repo.update(user)

    def _show_failed_login_messages(self, attempts_left: int) -> None:
        """Display appropriate flash messages based on remaining attempts."""
        if attempts_left > 0:
            message = f"Invalid password. {attempts_left} attempts remaining."
            FlashMessageHandler.warning(message)
        else:
            FlashMessageHandler.error("Account locked!")
            FlashMessageHandler.error("Please contact the administrator.")

    def handle_failed_login(self, user) -> None:
        user.failed_login_count += 1

        if user.failed_login_count >= self.MAX_LOGIN_ATTEMPTS:
            user.active = False

        self.auth_user_repo.update(user)

        attempts_left = self.MAX_LOGIN_ATTEMPTS - user.failed_login_count
        self._show_failed_login_messages(attempts_left)

    # def handle_tracking(self, ip: str, agent: str) -> None:
    #     user = current_user
    #     current_time = timezone_aware_datetime()
    #
    #     user.sign_in_count += 1
    #     user.last_sign_in_on = user.current_sign_in_on
    #     user.last_sign_in_ip = user.current_sign_in_ip
    #     user.last_user_agent = user.current_user_agent
    #
    #     user.current_sign_in_on = current_time
    #     user.current_sign_in_ip = ip
    #     user.current_user_agent = agent
    #
    #     self.auth_user_repo.update(user)

    def authenticate(self, username: str, password: str, remember: bool):
        # Validate inputs
        if not username or not password:
            FlashMessageHandler.error("Invalid username or password.")
            return None

        user = self.auth_user_repo.find_by_username(username)

        is_valid = False
        if user and user.is_active:
            is_valid = self.verify_password(user, password)

        if not user or not user.is_active:
            FlashMessageHandler.error("Invalid username or password.")
            return None

        if is_valid:
            login_user(user, remember=remember)

            if user.failed_login_count > 0:
                self.reset_failed_login_count(user)

            FlashMessageHandler.info(f"Welcome back {user.username}!")
            return user

        self.handle_failed_login(user)
        return None

    @staticmethod
    def logout() -> None:
        FlashMessageHandler.info("You have been logged out.")
        logout_user()
