from flask_login import login_user, logout_user, current_user
from .repository import AuthRepository


class AuthService:
    
    def __init__(self, repo=None):
        self.repo = repo or AuthRepository()
    
    
    def authenticate(self, email, password):
        user = self.repo.get_user_by_email(email)
        if user and user.check_password(password):
            login_user(user, force=True, remember=False)
            return user
        return None
    
    @staticmethod
    def logout():
        logout_user()
    
    @staticmethod
    def current_user():
        return current_user