from librepos.repositories.user_repository import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()
