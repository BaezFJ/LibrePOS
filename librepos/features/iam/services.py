import secrets

from librepos.common.base_service import BaseService
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
        data["password"] = self.generate_password()
        new_user = self.iam_user_repo.model_class(**data)
        return self.iam_user_repo.add(new_user)

    def create_group(self, data):
        new_group = self.iam_group_repo.model_class(**data)
        return self.iam_group_repo.add(new_group)
