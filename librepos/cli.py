import re
from pathlib import Path

import click

from librepos.iam.models import UserStatus


def add_cli_commands(app):  # noqa: PLR0915
    """Add custom commands to the Flask CLI."""

    from librepos.extensions import db  # noqa: PLC0415
    from librepos.iam.models import IAMRole, IAMUser  # noqa: PLC0415

    @app.cli.command("create-bp", help="Create a new blueprint.")
    @click.argument("blueprint_name")
    def create_bp(blueprint_name):
        """Create a new blueprint package directory with standard files."""
        if not re.match("^[a-z][a-z0-9_]*$", blueprint_name):
            click.echo(
                "Error: Blueprint name must be lowercase, start with a letter, and contain only letters, numbers, and underscores."
            )
            return

        bp_dir = Path("librepos") / blueprint_name
        if bp_dir.exists():
            click.echo(f"Error: Blueprint '{blueprint_name}' already exists.")
            return

        # Create a blueprint directory and __init__.py
        bp_dir.mkdir(parents=True)
        (bp_dir / "__init__.py").touch()

        # Create standard blueprint files
        standard_files = [
            "forms.py",
            "models.py",
            "routes.py",
            "views.py",
            "permissions.py",
        ]
        for file in standard_files:
            (bp_dir / file).write_text(f"# {blueprint_name} {file[:-3]} module\n")

        # Create templates directory structure
        templates_dir = bp_dir / "templates" / blueprint_name
        templates_dir.mkdir(parents=True)

        click.echo(f"Blueprint '{blueprint_name}' created successfully with standard files.")

    @app.cli.command("add-superuser", help="Add a superuser.")
    @click.option("--username", prompt=True, help="The username.", required=True)
    @click.option(
        "--password",
        prompt=True,
        hide_input=True,
        confirmation_prompt=True,
        help="The password.",
        required=True,
    )
    @click.option("--email", prompt=True, help="The email address.", required=True)
    @click.option("--first-name", prompt=True, help="The first name.", required=True)
    @click.option("--middle-name", prompt=True, help="The middle name.", required=False)
    @click.option("--last-name", prompt=True, help="The last name.", required=True)
    def add_superuser(username, password, email, first_name, middle_name, last_name):
        """Add a superuser."""
        click.echo("\nPlease confirm the following details:")
        click.echo(f"Username: {username}")
        click.echo(f"Password: {'*' * len(password)}")
        click.echo(f"Email: {email if email else '<empty>'}")
        click.echo(f"First name: {first_name}")
        click.echo(f"Middle name: {middle_name if middle_name else '<empty>'}")
        click.echo(f"Last name: {last_name}")

        if not click.confirm("\nDo you want to create this superuser?"):
            click.echo("Operation cancelled.")
            return

        IAMUser.create(
            username=username,
            email=email,
            unsecure_password=password,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            is_active=True,
            is_admin=True,
        )
        click.echo(f"Superuser '{username}' created successfully.")

    @app.cli.command("create-test-users", help="Create test users for development.")
    @click.option(
        "--users",
        "-u",
        multiple=True,
        type=click.Choice(
            ["owner", "admin", "manager", "cashier", "waiter", "customer"], case_sensitive=False
        ),
        help="Specific users to create. If not provided, all test users will be created.",
    )
    def create_test_users(users):
        """Create test users with different roles.

        If no users are specified, all default test users will be created.
        Use --users/-u to specify one or more users to create.

        Example:
            flask create-test-users
            flask create-test-users --users owner --users admin
            flask create-test-users -u cashier -u waiter
        """
        available_users = {
            "owner": {
                "role": "owner",
                "username": "owner",
                "email": "owner@test.com",
                "password": "owner123",
                "first_name": "Owner",
                "middle_name": "Test",
                "last_name": "User",
            },
            "admin": {
                "role": "admin",
                "username": "admin",
                "email": "admin@test.com",
                "password": "admin123",
                "first_name": "Admin",
                "middle_name": "Test",
                "last_name": "User",
            },
            "manager": {
                "role": "manager",
                "username": "manager",
                "email": "manager@test.com",
                "password": "manager123",
                "first_name": "Manager",
                "middle_name": "Test",
                "last_name": "User",
            },
            "cashier": {
                "role": "cashier",
                "username": "cashier",
                "email": "cashier@test.com",
                "password": "cashier123",
                "first_name": "Cashier",
                "middle_name": "Test",
                "last_name": "User",
            },
            "waiter": {
                "role": "waiter",
                "username": "waiter",
                "email": "waiter@test.com",
                "password": "waiter123",
                "first_name": "Waiter",
                "middle_name": "Test",
                "last_name": "User",
            },
            "customer": {
                "role": None,
                "username": "customer",
                "email": "customer@test.com",
                "password": "customer123",
                "first_name": "Customer",
                "middle_name": "Test",
                "last_name": "User",
            },
        }

        # Determine which users to create
        if users:
            users_to_create = [available_users[u.lower()] for u in users]
            click.echo(f"Creating {len(users_to_create)} test user(s)...")
        else:
            users_to_create = list(available_users.values())
            click.echo("Creating all test users...")

        created_count = 0
        skipped_count = 0

        for user_data in users_to_create:
            username = user_data["username"]
            if IAMUser.query.filter_by(username=username).first():
                click.echo(f"User '{username}' already exists. Skipping...")
                skipped_count += 1
                continue

            _role = IAMRole.get_first_by(slug=user_data.get("role", None))
            if not _role:
                click.echo(
                    f"Warning: Role '{user_data['role']}' not found. Skipping user '{username}'."
                )
                skipped_count += 1
                continue

            IAMUser.create(
                role_id=_role.id if _role else None,
                username=user_data["username"],
                email=user_data["email"],
                unsecure_password=user_data["password"],
                first_name=user_data["first_name"],
                middle_name=user_data["middle_name"],
                last_name=user_data["last_name"],
                status=user_data.get("status", UserStatus.ACTIVE),
            )
            click.echo(f"Created {username} (password: {user_data['password']})")
            created_count += 1

        click.echo(f"\nSummary: {created_count} created, {skipped_count} skipped")
        click.echo("Note: These users are for development/testing purposes only.")

    @app.cli.command(
        "seed-permissions", help="Seed groups, roles, permissions, and policies from blueprints."
    )
    def seed_permissions():
        """Seed groups, roles, permissions, and policies from blueprint permission files.

        This command auto-discovers permissions defined in each blueprint's permissions.py
        file and creates the necessary database records for:
        - Default groups (Employees, Suppliers, Customers)
        - Default roles (Admin, Manager, Cashier, etc.)
        - Permissions from all blueprints
        - Default policies with permission mappings
        """
        from librepos.permissions import seed_permissions_and_roles  # noqa: PLC0415

        click.echo("=" * 50)
        click.echo("Auto-seeding IAM infrastructure from blueprints...")
        click.echo("=" * 50)

        seed_permissions_and_roles(verbose=True)

    @app.cli.command(
        "sync-permissions", help="Sync permissions with code (add new, report orphaned)."
    )
    def sync_permissions():
        """Sync permissions in a database with permissions defined in code.

        This command:
        - Adds new permissions found in code
        - Reports orphaned permissions in a database (doesn't delete them)
        """
        from librepos.permissions import PermissionSeeder  # noqa: PLC0415

        click.echo("=" * 50)
        click.echo("Syncing permissions with code...")
        click.echo("=" * 50)

        seeder = PermissionSeeder()
        seeder.sync_permissions(verbose=True)

    @app.cli.command("reset-db", help="Reset the database.")
    def reset_db():
        """Reset the database."""
        db.drop_all()
        db.create_all()
        click.echo("Done!")
