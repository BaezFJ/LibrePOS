from enum import StrEnum

# Permission descriptions mapping
_DESCRIPTIONS = {
    # IAMUser
    "view:iam_user": "View IAM user details",
    "view:iam_user_self": "View own IAM user details",
    "list:iam_user": "List all IAM users",
    "create:iam_user": "Create new IAM users",
    "update:iam_user": "Update existing IAM users",
    "delete:iam_user": "Delete IAM users",
    # IAMGroup
    "view:iam_group": "View IAM group details",
    "list:iam_group": "List all IAM groups",
    "create:iam_group": "Create new IAM groups",
    "update:iam_group": "Update existing IAM groups",
    "delete:iam_group": "Delete IAM groups",
    # IAMPermission
    "view:iam_permission": "View IAM permission details",
    "list:iam_permission": "List all IAM permissions",
    "create:iam_permission": "Create new IAM permissions",
    "update:iam_permission": "Update existing IAM permissions",
    "delete:iam_permission": "Delete IAM permissions",
}


class IAMPermission(StrEnum):
    """IAMPermission Enum defining access control permissions.

    This enum defines the permissions used for IAM features across the application.

    Each permission follows the format: <action>: <resource> (e.g., create: iam_user)

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
    VIEW_IAM_USER = "view:iam_user"
    VIEW_IAM_USER_SELF = "view:iam_user_self"
    LIST_IAM_USER = "list:iam_user"
    CREATE_IAM_USER = "create:iam_user"
    UPDATE_IAM_USER = "update:iam_user"
    DELETE_IAM_USER = "delete:iam_user"

    # IAMGroup
    VIEW_IAM_GROUP = "view:iam_group"
    LIST_IAM_GROUP = "list:iam_group"
    CREATE_IAM_GROUP = "create:iam_group"
    UPDATE_IAM_GROUP = "update:iam_group"
    DELETE_IAM_GROUP = "delete:iam_group"

    # IAMPermission
    VIEW_IAM_PERMISSION = "view:iam_permission"
    LIST_IAM_PERMISSION = "list:iam_permission"
    CREATE_IAM_PERMISSION = "create:iam_permission"
    UPDATE_IAM_PERMISSION = "update:iam_permission"
    DELETE_IAM_PERMISSION = "delete:iam_permission"

    @property
    def description(self) -> str:
        return _DESCRIPTIONS[self.value]
