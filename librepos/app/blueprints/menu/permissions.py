"""Permission definitions for menu blueprint."""

from enum import StrEnum


class MenuPermissions(StrEnum):
    """Permissions for menu functionality."""

    VIEW = "view:menu"
    CREATE = "create:menu"
    EDIT = "edit:menu"
    DELETE = "delete:menu"
