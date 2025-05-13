from .repositories import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def get_all_users(self):
        return self._user_repo.get_all()

    def update_profile(self, user_id: int, **kwargs):
        return self._user_repo.update_profile(user_id, **kwargs)

    def update_password(self, user_id: int, new_password: str):
        return self._user_repo.update_password(user_id, new_password)
