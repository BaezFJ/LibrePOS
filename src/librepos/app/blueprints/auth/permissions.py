"""Permission definitions for auth blueprint."""
from enum import StrEnum


class AuthPermissions(StrEnum):
    """Permissions for auth functionality."""

    VIEW = "view:auth"
    CREATE = "create:auth"
    EDIT = "edit:auth"
    DELETE = "delete:auth"


# Policy definitions can be added here when the permissions system is set up
# AUTH_FULL_ACCESS = PolicyDefinition(
#     name="Auth Full Access",
#     description="Complete access to auth functionality",
#     permissions=list(AuthPermissions),
#     is_system=True,
# )
#
# DEFAULT_POLICIES = [AUTH_FULL_ACCESS]
