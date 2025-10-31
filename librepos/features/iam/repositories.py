from typing import Optional

from librepos.common.base_repository import BaseRepository
from .models import IAMUser, IAMPermission, IAMGroup, IAMUserProfile


class IAMUserRepository(BaseRepository[IAMUser]):
    def __init__(self):
        super().__init__(IAMUser)

    @staticmethod
    def find_by_username(username: str) -> Optional[IAMUser]:
        return IAMUser.query.filter_by(username=username).first()

    @staticmethod
    def user_has_permission(user: IAMUser, permission: str) -> bool:
        return permission in user.permissions

    @staticmethod
    def group_has_permission(group: IAMUser, permission: str) -> bool:
        return permission in group.permissions

    @staticmethod
    def is_superuser(user: IAMUser) -> bool:
        return bool(user.is_superuser)

    def create_user(self, data):
        new_user = IAMUser(**data)
        return self.add(new_user)


class IAMUserProfileRepository(BaseRepository[IAMUserProfile]):
    def __init__(self):
        super().__init__(IAMUserProfile)


class IAMPermissionRepository(BaseRepository[IAMPermission]):
    def __init__(self):
        super().__init__(IAMPermission)


class IAMGroupRepository(BaseRepository[IAMGroup]):
    def __init__(self):
        super().__init__(IAMGroup)

    def create_group(self, data):
        new_group = IAMGroup(**data)
        return self.add(new_group)
