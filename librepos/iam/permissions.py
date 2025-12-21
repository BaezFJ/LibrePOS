"""IAM (Identity and Access Management) blueprint permissions and policy mappings."""

from enum import StrEnum

from librepos.permissions import PolicyDefinition


class IAMPermissions(StrEnum):
    """Permissions for identity and access management functionality."""

    # User Management
    MANAGE_USERS = "manage_users"

    # Role & Permission Management
    MANAGE_ROLES = "manage_roles"
    MANAGE_PERMISSIONS = "manage_permissions"

    # Audit & Security
    VIEW_AUDIT_LOGS = "view_audit_logs"


# ============================================================================
# Default Policy Definitions
# ============================================================================

IAM_FULL_ACCESS_POLICY = PolicyDefinition(
    name="IAM Full Access",
    description="Complete access to all IAM functionality including user, role, and permission management",
    permissions=[
        IAMPermissions.MANAGE_USERS,
        IAMPermissions.MANAGE_ROLES,
        IAMPermissions.MANAGE_PERMISSIONS,
        IAMPermissions.VIEW_AUDIT_LOGS,
    ],
    is_system=True,
)

IAM_READ_ONLY_POLICY = PolicyDefinition(
    name="IAM Read Only",
    description="View-only access to audit logs and IAM information",
    permissions=[
        IAMPermissions.VIEW_AUDIT_LOGS,
    ],
    is_system=True,
)

# Collection of all default policies for this blueprint
DEFAULT_POLICIES = [
    IAM_FULL_ACCESS_POLICY,
    IAM_READ_ONLY_POLICY,
]
