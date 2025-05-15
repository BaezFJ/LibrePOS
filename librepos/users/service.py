from .repository import UserRepository


class UserService:

    def __init__(self, repo=None):
        self.repo = repo or UserRepository()

    def list_users(self):
        return self.repo.get_all()

    def get_user(self, user_id):
        return self.repo.get_by_id(user_id)
