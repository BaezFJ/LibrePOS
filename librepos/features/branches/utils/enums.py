from enum import StrEnum


class BranchPermissions(StrEnum):
    """Branch Management Permissions Enum defining access control permissions.

    This enum defines the permissions used for Branch Management functionality
    across the application.

    The permissions are organized into the following categories:
    - Base access: General branch management access permission
    - Branch: Permissions for managing branch locations

    Each permission follows the format: branch.<action>.<resource>

    Example usage:
        @permission_required(BranchPermissions.CREATE_BRANCH)
        def create_branch():
            # Function implementation
            pass

        # Compare permissions
        if user_permission == BranchPermissions.READ_BRANCH:
            # Handle read branch permission
            pass
    """

    # Bae access
    ACCESS = "branch.allow.access"

    # Branch
    CREATE_BRANCH = "branch.create.branch"
    READ_BRANCH = "branch.read.branch"
    LIST_BRANCH = "branch.list.branch"
    UPDATE_BRANCH = "branch.update.branch"
    DELETE_BRANCH = "branch.delete.branch"
