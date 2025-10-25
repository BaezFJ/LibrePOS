from typing import Optional

from librepos.common.base_service import BaseService
from .models import IAMUser, IAMUserGroup
from .repositories import (
    IAMUserRepository,
    IAMPermissionRepository,
    IAMUserGroupRepository,
)


class IAMService(BaseService):
    def __init__(self):
        self.iam_user_repo = IAMUserRepository()
        self.iam_permission_repo = IAMPermissionRepository()
        self.iam_user_group_repo = IAMUserGroupRepository()

    def create_user(self, data) -> Optional[IAMUser]:
        data["password"] = "test"
        new_user = self.iam_user_repo.model_class(**data)
        return self._create_entity(
            entity=new_user,
            repository=self.iam_user_repo,
            success_message="User created successfully.",
            error_message="Failed to create user.",
        )

    def create_group(self, data) -> Optional[IAMUserGroup]:
        new_group = self.iam_user_group_repo.model_class(**data)
        return self._create_entity(
            entity=new_group,
            repository=self.iam_user_group_repo,
            success_message="Group created successfully.",
            error_message="Failed to create group.",
        )
