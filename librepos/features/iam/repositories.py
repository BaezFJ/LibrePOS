from sqlalchemy.orm import InstrumentedAttribute

from librepos.common.base_repository import BaseRepository

from .models import IAMUser, IAMPermission, IAMUserGroup


class IAMUserRepository(BaseRepository[IAMUser]):
    def __init__(self):
        super().__init__(IAMUser)

    @staticmethod
    def find_by_username(username: str) -> IAMUser:
        return IAMUser.query.filter_by(username=username).first()

    @staticmethod
    def user_has_permission(user: IAMUser, permission: str) -> bool:
        return permission in user.permissions

    @staticmethod
    def group_has_permission(group: IAMUser, permission: str) -> bool:
        return permission in group.permissions

    @staticmethod
    def is_superuser(user: IAMUser) -> InstrumentedAttribute[bool]:
        return user.is_superuser


class IAMPermissionRepository(BaseRepository[IAMPermission]):
    def __init__(self):
        super().__init__(IAMPermission)


class IAMUserGroupRepository(BaseRepository[IAMUserGroup]):
    def __init__(self):
        super().__init__(IAMUserGroup)
