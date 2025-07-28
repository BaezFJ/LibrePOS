from enum import StrEnum


class IAMPermissions(StrEnum):
    """IAM Permissions Enum defining access control permissions.

    This enum defines the permissions used for Identity and Access Management (IAM)
    across the application.

    The permissions are organized into the following categories:
    - Base access: General system access permission
    - User: Permissions for managing user accounts
    - Role: Permissions for managing roles
    - Policy: Permissions for managing access policies

    Each permission follows the format: iam.<action>.<resource>

    Example usage:
        @permission_required(IAMPermissions.CREATE_USER)
        def create_user():
            # Function implementation
            pass

        # Compare permissions
        if user_permission == IAMPermissions.READ_USER:
            # Handle read user permission
            pass
    """

    # Base access
    ACCESS = "iam.allow.access"

    # User
    CREATE_USER = "iam.create.user"
    READ_USER = "iam.read.user"
    LIST_USER = "iam.list.user"
    UPDATE_USER = "iam.update.user"
    DELETE_USER = "iam.delete.user"

    # Role
    CREATE_ROLE = "iam.create.role"
    READ_ROLE = "iam.read.role"
    LIST_ROLE = "iam.list.role"
    UPDATE_ROLE = "iam.update.role"
    DELETE_ROLE = "iam.delete.role"

    # Policy
    CREATE_POLICY = "iam.create.policy"
    READ_POLICY = "iam.read.policy"
    LIST_POLICY = "iam.list.policy"
    UPDATE_POLICY = "iam.update.policy"
    DELETE_POLICY = "iam.delete.policy"
