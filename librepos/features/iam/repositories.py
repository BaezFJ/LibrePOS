from typing import Optional

from sqlalchemy import select

from librepos.core.repository import BaseRepository
from librepos.core.extensions import db

from .models import IAMUser, IAMPermission, IAMGroup, IAMUserProfile, IAMPermissionCategory


class IAMUserRepository(BaseRepository[IAMUser]):
    def __init__(self):
        super().__init__(IAMUser, db.session)

    @staticmethod
    def find_by_username(username: str) -> Optional[IAMUser]:
        return db.session.execute(select(IAMUser).filter_by(username=username)).scalars().first()

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
        super().__init__(IAMUserProfile, db.session)


class IAMPermissionRepository(BaseRepository[IAMPermission]):
    def __init__(self):
        super().__init__(IAMPermission, db.session)


class IAMGroupRepository(BaseRepository[IAMGroup]):
    def __init__(self):
        super().__init__(IAMGroup, db.session)

    def create_group(self, data):
        new_group = IAMGroup(**data)
        return self.add(new_group)


class IAMPermissionCategoryRepository(BaseRepository[IAMPermissionCategory]):
    def __init__(self):
        super().__init__(IAMPermissionCategory, db.session)
