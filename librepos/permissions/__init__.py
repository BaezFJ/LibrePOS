"""Permission management infrastructure.

This package contains the permission registry and seeding functionality
that auto-discovers permissions from all blueprints.
"""

from enum import StrEnum
from typing import NamedTuple

from .registry import PermissionRegistry, get_registry
from .seeder import PermissionSeeder, seed_permissions_and_roles


class PolicyDefinition(NamedTuple):
    """Definition of a policy with its metadata.

    Used to define default policies in blueprint permission modules.

    Attributes:
        name: Human-readable name of the policy
        description: Description of what access this policy grants
        permissions: List of permission enum values included in this policy
        is_system: Whether this is a system-managed policy (cannot be deleted)

    Example:
        >>> ADMIN_POLICY = PolicyDefinition(
        ...     name="Admin Full Access",
        ...     description="Complete administrative access",
        ...     permissions=[
        ...         MyPermissions.CREATE,
        ...         MyPermissions.READ,
        ...         MyPermissions.UPDATE,
        ...         MyPermissions.DELETE,
        ...     ],
        ...     is_system=True,
        ... )
    """

    name: str
    description: str
    permissions: list[StrEnum]
    is_system: bool = True


__all__ = [
    "PermissionRegistry",
    "PermissionSeeder",
    "PolicyDefinition",
    "get_registry",
    "seed_permissions_and_roles",
]
