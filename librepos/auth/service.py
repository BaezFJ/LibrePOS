from flask_login import login_user, logout_user, current_user
from flask import flash
from .repository import AuthRepository


class AuthService:
    def __init__(self, repo=None):
        self.repo = repo or AuthRepository()

    def authenticate(self, email, password, remember):
        user = self.repo.get_user_by_email(email)
        if not user:
            flash("Invalid email or password.", "error")
            return None
        if not user.active:
            flash("Your account has been deactivated. Please contact support.", "error")
            return None
        if user.check_password(password):
            login_user(user, remember=remember)
            if user.failed_login_count > 0:
                user.reset_failed_login_count()
            flash("Logged in successfully.", "success")
            return user
        user.handle_failed_login()
        attempts_left = 3 - user.failed_login_count
        if attempts_left > 0:
            flash(
                f"Invalid password. {attempts_left} attempts remaining before account lockout.",
                "warning",
            )
        else:
            flash(
                "Account locked due to too many failed login attempts. Please contact support.",
                "error",
            )
        return None

    @staticmethod
    def logout():
        logout_user()

    @staticmethod
    def current_user():
        return current_user
