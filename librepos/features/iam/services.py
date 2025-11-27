import secrets

from librepos.core.service import BaseService
from .repositories import (
    IAMUserRepository,
    IAMGroupRepository,
    IAMUserProfileRepository,
    IAMPermissionRepository,
)


class IAMService(BaseService):
    def __init__(self):
        self.iam_user_repo = IAMUserRepository()
        self.iam_group_repo = IAMGroupRepository()
        self.iam_user_profile_repo = IAMUserProfileRepository()
        self.iam_permission_repo = IAMPermissionRepository()

    @staticmethod
    def generate_password(length: int = 16) -> str:
        return secrets.token_urlsafe(length)

    def create_user(self, data):
        def operation():
            data["password"] = self.generate_password()
            new_user = self.iam_user_repo.model(**data)
            return self.iam_user_repo.add(new_user)

        return self._execute_with_error_handling(operation, "Failed to create user.")

    def create_group(self, data):
        def operation():
            new_group = self.iam_group_repo.model(**data)
            return self.iam_group_repo.add(new_group)

        return self._execute_with_error_handling(operation, "Failed to create group.")
