"""Auto-seeder for permissions and role-permission mappings.

This module provides functionality to automatically seed the database
with permissions and role-permission mappings discovered from blueprints.
"""

import click

from .registry import get_registry

# Default roles to seed
DEFAULT_ROLES = [
    {
        "name": "Owner",
        "description": "Owner role with full access to all features",
        "is_staff_role": True,
        "is_system": True,
    },
    {
        "name": "Admin",
        "description": "Administrative role with extensive permissions",
        "is_staff_role": True,
        "is_system": True,
    },
    {
        "name": "Manager",
        "description": "Manager role with operational control",
        "is_staff_role": True,
    },
    {
        "name": "Cashier",
        "description": "Cashier role for POS and payment operations",
        "is_staff_role": True,
    },
    {
        "name": "Waiter",
        "description": "Server/waiter role for taking orders and serving",
        "is_staff_role": True,
    },
    {
        "name": "Bartender",
        "description": "Bartender role for bar operations",
        "is_staff_role": True,
    },
    {
        "name": "Kitchen Staff",
        "description": "Kitchen staff role for food preparation",
        "is_staff_role": True,
    },
    {
        "name": "Host",
        "description": "Host/hostess role for guest management",
        "is_staff_role": True,
    },
    {
        "name": "Delivery Driver",
        "description": "Delivery driver role for order delivery",
        "is_staff_role": True,
    },
]


class PermissionSeeder:
    """Handles automatic seeding of permissions and role-permission mappings."""

    def __init__(self):
        self.registry = get_registry()
        self.created_count = 0
        self.skipped_count = 0
        self.error_count = 0

    def seed_roles(self, verbose: bool = True) -> int:
        """Seed default roles into the database.

        Args:
            verbose: Whether to print progress messages

        Returns:
            Number of roles created
        """
        # Import here to avoid circular dependency
        from librepos.iam.models import IAMRole  # noqa: PLC0415

        if verbose:
            click.echo("\nSeeding default roles...")

        created = 0

        for role_data in DEFAULT_ROLES:
            # Check if role already exists
            existing = IAMRole.get_first_by(name=role_data["name"])

            if existing:
                self.skipped_count += 1
                continue

            try:
                # Create a new role
                IAMRole.create(
                    name=role_data["name"],
                    description=role_data.get("description"),
                    is_staff_role=role_data.get("is_staff_role", False),
                    is_system=role_data.get("is_system", False),
                )
                created += 1
                self.created_count += 1

                if verbose:
                    click.echo(f"  ✓ Created role: {role_data['name']}")

            except Exception as e:
                self.error_count += 1
                if verbose:
                    click.echo(f"  ✗ Error creating role '{role_data['name']}': {e}")

        return created

    def seed_permissions(self, verbose: bool = True) -> int:
        """Seed all permissions from the registry into the database.

        Args:
            verbose: Whether to print progress messages

        Returns:
            Number of permissions created
        """
        # Import here to avoid circular dependency
        from librepos.iam.models import IAMPermission  # noqa: PLC0415

        if verbose:
            click.echo("Seeding permissions...")

        all_permissions = self.registry.get_all_permissions()
        created = 0

        for perm_name in all_permissions:
            # Check if permission already exists
            existing = IAMPermission.get_first_by(name=perm_name)

            if existing:
                self.skipped_count += 1
                continue

            try:
                # Create new permission
                IAMPermission.create(name=perm_name)
                created += 1
                self.created_count += 1

                if verbose:
                    click.echo(f"  ✓ Created permission: {perm_name}")

            except Exception as e:
                self.error_count += 1
                if verbose:
                    click.echo(f"  ✗ Error creating permission '{perm_name}': {e}")

        return created

    def seed_policies(self, verbose: bool = True) -> int:  # noqa: PLR0912
        """Seed default policies from blueprint permission modules.

        Args:
            verbose: Whether to print progress messages

        Returns:
            Number of policies created
        """
        # Import here to avoid circular dependency
        from librepos.iam.models import (  # noqa: PLC0415
            IAMPermission,
            IAMPolicy,
            IAMPolicyPermission,
        )

        if verbose:
            click.echo("\nSeeding default policies...")

        default_policies = self.registry.get_default_policies()
        policies_created = 0

        for policy_def in default_policies:
            # Check if policy already exists
            existing_policy = IAMPolicy.get_first_by(name=policy_def.name)

            if existing_policy:
                self.skipped_count += 1
                if verbose:
                    click.echo(f"  ⊙ Policy '{policy_def.name}' already exists. Skipping...")
                continue

            try:
                # Create the policy
                policy = IAMPolicy.create(
                    name=policy_def.name,
                    description=policy_def.description,
                    is_system=policy_def.is_system,
                )
                policies_created += 1
                self.created_count += 1

                if verbose:
                    click.echo(f"  ✓ Created policy: {policy_def.name}")

                # Type checker hint: policy.id is set after create and commit
                policy_id: int = policy.id  # type: ignore[assignment]

                # Add permissions to the policy
                permissions_added = 0
                for perm_enum in policy_def.permissions:
                    # Get permission name from enum
                    perm_name = perm_enum.value if hasattr(perm_enum, "value") else str(perm_enum)

                    # Get the permission from database
                    permission = IAMPermission.get_first_by(name=perm_name)
                    if not permission:
                        if verbose:
                            click.echo(
                                f"    ⚠ Warning: Permission '{perm_name}' not found. Skipping..."
                            )
                        self.error_count += 1
                        continue

                    # Type checker hint: permission.id is set after retrieval
                    permission_id: int = permission.id  # type: ignore[assignment]

                    # Check if policy-permission mapping already exists
                    existing_mapping = IAMPolicyPermission.get_first_by(
                        policy_id=policy_id, permission_id=permission_id
                    )

                    if existing_mapping:
                        continue

                    try:
                        # Create policy-permission mapping
                        IAMPolicyPermission.create(policy_id=policy_id, permission_id=permission_id)
                        permissions_added += 1

                    except Exception as e:
                        self.error_count += 1
                        if verbose:
                            click.echo(
                                f"    ✗ Error adding permission '{perm_name}' to policy: {e}"
                            )

                if verbose and permissions_added > 0:
                    click.echo(f"    → Added {permissions_added} permissions to policy")

            except Exception as e:
                self.error_count += 1
                if verbose:
                    click.echo(f"  ✗ Error creating policy '{policy_def.name}': {e}")

        return policies_created

    def associate_owner_with_full_access_policies(self, verbose: bool = True) -> int:
        """Associate the Owner role with all policies containing '_FULL_ACCESS' in their name.

        Args:
            verbose: Whether to print progress messages

        Returns:
            Number of role-policy associations created
        """
        # Import here to avoid circular dependency
        from librepos.iam.models import IAMPolicy, IAMRole, IAMRolePolicy  # noqa: PLC0415

        if verbose:
            click.echo("\nAssociating Owner role with FULL_ACCESS policies...")

        # Get the Owner role
        owner_role = IAMRole.get_first_by(name="Owner")
        if not owner_role:
            if verbose:
                click.echo("  ⚠ Warning: Owner role not found. Skipping...")
            self.error_count += 1
            return 0

        # Get all policies with '_FULL_ACCESS' in their name
        full_access_policies = IAMPolicy.query.filter(IAMPolicy.name.contains("_FULL_ACCESS")).all()

        if not full_access_policies:
            if verbose:
                click.echo("  ⊙ No FULL_ACCESS policies found.")
            return 0

        created = 0
        for policy in full_access_policies:
            # Check if association already exists
            existing = IAMRolePolicy.get_first_by(role_id=owner_role.id, policy_id=policy.id)

            if existing:
                self.skipped_count += 1
                continue

            try:
                # Create role-policy association
                IAMRolePolicy.create(role_id=owner_role.id, policy_id=policy.id)
                created += 1
                self.created_count += 1

                if verbose:
                    click.echo(f"  ✓ Associated policy '{policy.name}' with Owner role")

            except Exception as e:
                self.error_count += 1
                if verbose:
                    click.echo(f"  ✗ Error associating policy '{policy.name}': {e}")

        return created

    def seed_role_permissions(self, verbose: bool = True) -> int:
        """Seed role-permission mappings from the registry (legacy).

        Args:
            verbose: Whether to print progress messages

        Returns:
            Number of role-permission mappings created
        """
        # Import here to avoid circular dependency
        from librepos.iam.models import IAMPermission, IAMRole, IAMRolePermission  # noqa: PLC0415

        if verbose:
            click.echo("\nSeeding role-permission mappings (legacy)...")

        role_mappings = self.registry.get_role_permissions_mapping()
        created = 0

        for role_name, permission_names in role_mappings.items():
            # Get the role
            role = IAMRole.get_first_by(name=role_name)
            if not role:
                if verbose:
                    click.echo(f"  ⚠ Warning: Role '{role_name}' not found. Skipping...")
                self.error_count += 1
                continue

            for perm_name in permission_names:
                # Get the permission
                permission = IAMPermission.get_first_by(name=perm_name)
                if not permission:
                    if verbose:
                        click.echo(f"  ⚠ Warning: Permission '{perm_name}' not found. Skipping...")
                    self.error_count += 1
                    continue

                # Check if mapping already exists
                existing = IAMRolePermission.get_first_by(
                    role_id=role.id, permission_id=permission.id
                )

                if existing:
                    self.skipped_count += 1
                    continue

                try:
                    # Create role-permission mapping
                    IAMRolePermission.create(role_id=role.id, permission_id=permission.id)
                    created += 1
                    self.created_count += 1

                except Exception as e:
                    self.error_count += 1
                    if verbose:
                        click.echo(f"  ✗ Error mapping '{perm_name}' to '{role_name}': {e}")

        return created

    def seed_all(self, verbose: bool = True):
        """Seed groups, roles, permissions, policies, and role-permission mappings.

        Args:
            verbose: Whether to print progress messages
        """
        # Reset counters
        self.created_count = 0
        self.skipped_count = 0
        self.error_count = 0

        # Seed roles
        self.seed_roles(verbose=verbose)

        # Seed permissions
        self.seed_permissions(verbose=verbose)

        # Seed default policies
        self.seed_policies(verbose=verbose)

        # Associate Owner role with FULL_ACCESS policies
        self.associate_owner_with_full_access_policies(verbose=verbose)

        # Then seed legacy role-permission mappings (if any exist)
        self.seed_role_permissions(verbose=verbose)

        if verbose:
            click.echo("\n" + "=" * 50)
            click.echo("Seeding complete!")
            click.echo(f"  Created: {self.created_count}")
            click.echo(f"  Skipped (already exist): {self.skipped_count}")
            if self.error_count > 0:
                click.echo(f"  Errors: {self.error_count}")

    def sync_permissions(self, verbose: bool = True):
        """Sync permissions - add new ones, optionally remove orphaned ones.

        This is useful for keeping the database in sync with code changes.

        Args:
            verbose: Whether to print progress messages
        """
        # Import here to avoid circular dependency
        from librepos.iam.models import IAMPermission  # noqa: PLC0415

        if verbose:
            click.echo("Syncing permissions with code...")

        # Get all permissions from code
        code_permissions = set(self.registry.get_all_permissions())

        # Get all permissions from a database
        db_permissions = {p.name for p in IAMPermission.query.all()}

        # Find new permissions to add
        new_permissions = code_permissions - db_permissions
        if new_permissions:
            if verbose:
                click.echo(f"\nFound {len(new_permissions)} new permissions to add:")
            for perm_name in sorted(new_permissions):
                try:
                    IAMPermission.create(name=perm_name)
                    if verbose:
                        click.echo(f"  ✓ Added: {perm_name}")
                except Exception as e:
                    if verbose:
                        click.echo(f"  ✗ Error adding '{perm_name}': {e}")

        # Find orphaned permissions in database
        orphaned_permissions = db_permissions - code_permissions
        if orphaned_permissions and verbose:
            click.echo(f"\n⚠ Found {len(orphaned_permissions)} orphaned permissions in database:")
            for perm_name in sorted(orphaned_permissions):
                click.echo(f"  • {perm_name}")
            click.echo("\nNote: Orphaned permissions are NOT automatically deleted.")
            click.echo("Remove them manually if they're no longer needed.")

        if not new_permissions and not orphaned_permissions and verbose:
            click.echo("  ✓ All permissions are in sync!")


def seed_permissions_and_roles(verbose: bool = True):
    """Convenience function to seed all groups, roles, permissions, and policies.

    Args:
        verbose: Whether to print progress messages
    """
    seeder = PermissionSeeder()
    seeder.seed_all(verbose=verbose)
