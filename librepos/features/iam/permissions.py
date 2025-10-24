from enum import StrEnum


class IAMPermissions(StrEnum):
    """IAMPermissions Enum defining access control permissions.

    This enum defines the permissions used for IAM features across the application.

    Each permission follows the format: <feature_label>.<action>_<model_name> (e.g., iam.create_iam_user)

    Example usage:
        @permission_required(IAMPermission.CREATE_IAM_USER)
        def create_user():
            # Function implementation
            pass

        # Compare permissions
        if user_permission == IAMPermission.VIEW_IAM_USER:
            # Handle read user permission
            pass
    """

    # IAMUser
    VIEW_IAM_USER = "iam.view_iam_user"
    CREATE_IAM_USER = "iam.create_iam_user"
    UPDATE_IAM_USER = "iam.update_iam_user"
    DELETE_IAM_USER = "iam.delete_iam_user"

    # IAMGroup
    VIEW_IAM_GROUP = "iam.view_iam_group"
    CREATE_IAM_GROUP = "iam.create_iam_group"
    UPDATE_IAM_GROUP = "iam.update_iam_group"
    DELETE_IAM_GROUP = "iam.delete_iam_group"

    # IAMPermission
    VIEW_IAM_PERMISSION = "iam.view_iam_permission"

    @property
    def description(self) -> str:
        return _DESCRIPTIONS[self]


_DESCRIPTIONS: dict[IAMPermissions, str] = {
    # IAMUser
    IAMPermissions.VIEW_IAM_USER: "View complete user profile information including assigned roles, permissions and account details",
    IAMPermissions.CREATE_IAM_USER: "Create new user account with specific roles and permissions",
    IAMPermissions.UPDATE_IAM_USER: "Modify existing user profiles including roles, permissions, contact information and account status",
    IAMPermissions.DELETE_IAM_USER: "Permanently remove user accounts from the system.",
    # IAMGroup
    IAMPermissions.VIEW_IAM_GROUP: "View complete group information including assigned roles and permissions",
    IAMPermissions.CREATE_IAM_GROUP: "Create new group with specific roles and permissions",
    IAMPermissions.UPDATE_IAM_GROUP: "Modify existing group configurations including adding/removing permissions and access levels",
    IAMPermissions.DELETE_IAM_GROUP: "Permanently remove groups from the system and unassign them from all associated users",
    # IAMPermission
    IAMPermissions.VIEW_IAM_PERMISSION: "View complete permission information.",
}
