from enum import StrEnum
from typing import List, Type


class PermissionLevelManager:
    """
    Generic utility class for managing permission levels across different permission enums.
    Provides methods to build permission hierarchies (read-only, limited, full access)
    for any permission enum that follows the standard pattern.

    This class operates on StrEnum permission enums that follow the naming convention:
    - READ_* for read permissions
    - LIST_* for list permissions
    - UPDATE_* for update permissions
    - CREATE_* for creation permissions
    - DELETE_* for delete permissions
    - ACCESS for base access permission

    Example Usage:
        class UserPermissions(StrEnum):
            ACCESS = "user.access"
            CREATE_USER = "user.create"
            READ_USER = "user.read"
            LIST_USER = "user.list"
            UPDATE_USER = "user.update"
            DELETE_USER = "user.delete"

        # Get read-only permissions (ACCESS, READ_*, LIST_*)
        read_perms = PermissionLevelManager.get_read_only_permissions(UserPermissions)
        # ['user.access', 'user.read', 'user.list']

        # Get limited access - read and update permissions
        limited_perms = PermissionLevelManager.get_limited_access_permissions(UserPermissions)
        # ['user.access', 'user.read', 'user.list', 'user.update']

        # Get full access - read + update + create/delete permissions
        full_perms = PermissionLevelManager.get_full_access_permissions(UserPermissions)
        # ['user.access', 'user.read', 'user.list', 'user.update', 'user.create', 'user.delete']

        # Add specific additional permissions
        custom_perms = PermissionLevelManager.get_limited_access_permissions(
            UserPermissions,
            additional_permissions=['user.create'])
        # ['user.access', 'user.read', 'user.list', 'user.update', 'user.create']
    """

    @staticmethod
    def build_permission_list(
            base_permissions: List[str], additional_permissions: List[str]
    ) -> List[str]:
        """Helper method to build permission lists efficiently"""
        result = list(base_permissions)
        result.extend(additional_permissions)
        return result

    @staticmethod
    def get_read_only_permissions(permission_enum: Type[StrEnum]) -> List[str]:
        """
        Get all read-only permissions for a given permission enum.
        Includes ACCESS, READ_*, and LIST_* permissions.
        """
        permissions = []

        # Get all enum members and filter for READ, LIST and ACCESS permissions
        for member in permission_enum:
            member_name = member.name
            if (
                    member_name.startswith("READ_")
                    or member_name.startswith("LIST_")
                    or member_name == "ACCESS"
            ):
                permissions.append(member.value)

        return permissions

    @staticmethod
    def get_limited_access_permissions(
            permission_enum: Type[StrEnum], additional_permissions: List[str] | None = None
    ) -> List[str]:
        """
        Get limited access permissions for a given permission enum.
        Includes read-only permissions plus specified UPDATE permissions.
        """
        base_permissions = PermissionLevelManager.get_read_only_permissions(
            permission_enum
        )

        if additional_permissions is None:
            # Default to all UPDATE permissions
            additional_permissions = []
            for member in permission_enum:
                if member.name.startswith("UPDATE_"):
                    additional_permissions.append(member.value)

        return PermissionLevelManager.build_permission_list(
            base_permissions, additional_permissions
        )

    @staticmethod
    def get_full_access_permissions(
            permission_enum: Type[StrEnum], additional_permissions: List[str] | None = None
    ) -> List[str]:
        """
        Get full access permissions for a given permission enum.
        Includes limited access permissions plus specified CREATE and DELETE permissions.
        """
        base_permissions = PermissionLevelManager.get_limited_access_permissions(
            permission_enum
        )

        if additional_permissions is None:
            # Default to all CREATE and DELETE permissions
            additional_permissions = []
            for member in permission_enum:
                if member.name.startswith("CREATE_") or member.name.startswith(
                        "DELETE_"
                ):
                    additional_permissions.append(member.value)

        return PermissionLevelManager.build_permission_list(
            base_permissions, additional_permissions
        )
