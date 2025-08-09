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

    @property
    def description(self) -> str:
        return _DESCRIPTIONS[self]


_DESCRIPTIONS: dict[IAMPermissions, str] = {
    IAMPermissions.ACCESS: "View and navigate the Identity and Access Management (IAMPermissions) interface for managing users, roles and permissions",
    IAMPermissions.CREATE_USER: "Create new user accounts and assign them specific roles and permissions for system access",
    IAMPermissions.READ_USER: "View complete user profile information including assigned roles, permissions and account details",
    IAMPermissions.LIST_USER: "View and search through the complete list of system users with their assigned roles and status",
    IAMPermissions.UPDATE_USER: "Modify existing user profiles including roles, permissions, contact information and account status",
    IAMPermissions.DELETE_USER: "Permanently remove user accounts and revoke all associated system access privileges",
    IAMPermissions.CREATE_ROLE: "Define new roles with specific sets of permissions that can be assigned to multiple users",
    IAMPermissions.READ_ROLE: "View detailed role configurations including all associated permissions and access levels",
    IAMPermissions.LIST_ROLE: "View and search through all system roles and their assigned permissions and user assignments",
    IAMPermissions.UPDATE_ROLE: "Modify existing role configurations including adding/removing permissions and access levels",
    IAMPermissions.DELETE_ROLE: "Permanently remove roles from the system and unassign them from all associated users",
}
