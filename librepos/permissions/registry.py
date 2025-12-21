"""Permission Registry - Auto-discovers permissions from all blueprints.

This module provides a centralized registry that automatically discovers
permissions defined in each blueprint's permissions.py file.
"""

from typing import Dict, List, Set
import importlib
import pkgutil
from pathlib import Path


class PermissionRegistry:
    """Central registry for auto-discovering and managing permissions across blueprints."""

    def __init__(self):
        self._permissions: Dict[str, Set[str]] = {}
        self._policy_mappings: Dict[str, Dict[str, List[str]]] = {}
        self._discovered = False

    def discover(self):
        """Discover all permissions from blueprint permission modules."""
        if self._discovered:
            return

        # Get the librepos package directory
        import librepos

        librepos_path = Path(librepos.__file__).parent

        # Scan all subdirectories for permissions.py files
        for module_info in pkgutil.iter_modules([str(librepos_path)]):
            blueprint_name = module_info.name

            # Skip non-blueprint modules
            if blueprint_name in [
                "utils",
                "extensions",
                "config",
                "app",
                "cli",
                "permissions",
                "ui",
            ]:
                continue

            try:
                # Try to import the permissions module
                permissions_module = importlib.import_module(
                    f"librepos.{blueprint_name}.permissions"
                )

                # Extract permissions and policy mapping
                self._load_blueprint_permissions(blueprint_name, permissions_module)

            except (ImportError, AttributeError):
                # Blueprint doesn't have a permissions.py file, skip it
                continue

        self._discovered = True

    def _load_blueprint_permissions(self, blueprint_name: str, module):
        """Load permissions and policy mappings from a blueprint's permissions module."""
        permissions = set()

        # Find all permission classes (classes ending with 'Permissions')
        for attr_name in dir(module):
            attr = getattr(module, attr_name)

            # Check if it's a class with permission constants
            if isinstance(attr, type) and attr_name.endswith("Permissions"):
                # Get all uppercase attributes (permissions)
                for perm_name in dir(attr):
                    if perm_name.isupper() and not perm_name.startswith("_"):
                        perm_value = getattr(attr, perm_name)
                        if isinstance(perm_value, str):
                            permissions.add(perm_value)

        # Store permissions for this blueprint
        if permissions:
            self._permissions[blueprint_name] = permissions

        # Load policy mapping if it exists (legacy)
        if hasattr(module, "POLICY_MAPPING"):
            policy_mapping = getattr(module, "POLICY_MAPPING")
            if isinstance(policy_mapping, dict):
                self._policy_mappings[blueprint_name] = policy_mapping

    def get_all_permissions(self) -> List[str]:
        """Get a flat list of all permissions across all blueprints."""
        self.discover()
        all_perms = set()
        for perms in self._permissions.values():
            all_perms.update(perms)
        return sorted(list(all_perms))

    def get_blueprint_permissions(self, blueprint_name: str) -> List[str]:
        """Get permissions for a specific blueprint."""
        self.discover()
        return sorted(list(self._permissions.get(blueprint_name, set())))

    def get_role_permissions_mapping(self) -> Dict[str, List[str]]:
        """Aggregate all role-permission mappings from all blueprints.

        Returns:
            Dict mapping role names to lists of permission names.
        """
        self.discover()

        # Aggregate mappings from all blueprints
        aggregated: Dict[str, Set[str]] = {}

        for blueprint_name, policy_mapping in self._policy_mappings.items():
            for role, permissions in policy_mapping.items():
                # Convert role enum to string if needed
                from enum import Enum

                role_name = role.value if isinstance(role, Enum) else str(role)

                if role_name not in aggregated:
                    aggregated[role_name] = set()

                # Add permissions for this role
                if isinstance(permissions, (list, set, tuple)):
                    aggregated[role_name].update(permissions)

        # Convert sets to sorted lists
        return {role: sorted(list(perms)) for role, perms in aggregated.items()}

    def get_blueprints_with_permissions(self) -> List[str]:
        """Get list of blueprint names that have permissions defined."""
        self.discover()
        return sorted(list(self._permissions.keys()))

    def get_default_policies(self) -> List:
        """Get all default policy definitions from all blueprints.

        Returns:
            List of PolicyDefinition objects from all blueprints.
        """
        self.discover()

        import librepos

        librepos_path = Path(librepos.__file__).parent

        policies = []

        # Scan all subdirectories for permissions.py files
        for module_info in pkgutil.iter_modules([str(librepos_path)]):
            blueprint_name = module_info.name

            # Skip non-blueprint modules
            if blueprint_name in [
                "utils",
                "extensions",
                "config",
                "app",
                "cli",
                "permissions",
                "ui",
            ]:
                continue

            try:
                # Try to import the permissions module
                permissions_module = importlib.import_module(
                    f"librepos.{blueprint_name}.permissions"
                )

                # Check if DEFAULT_POLICIES exists
                if hasattr(permissions_module, "DEFAULT_POLICIES"):
                    default_policies = getattr(permissions_module, "DEFAULT_POLICIES")
                    if isinstance(default_policies, list):
                        policies.extend(default_policies)

            except (ImportError, AttributeError):
                # Blueprint doesn't have a permissions.py file, skip it
                continue

        return policies


# Global registry instance
_registry = None


def get_registry() -> PermissionRegistry:
    """Get the global permission registry instance."""
    global _registry
    if _registry is None:
        _registry = PermissionRegistry()
    return _registry
