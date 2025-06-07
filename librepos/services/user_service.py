from librepos.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()

    def list_users(self):
        return self.user_repository.get_all()

    def get_user(self, user_id):
        return self.user_repository.get_by_id(user_id)

    def create_user(self, data):
        return self.user_repository.create(data)

    def update_user(self, user_id, data):
        return self.user_repository.update(user_id, **data)
