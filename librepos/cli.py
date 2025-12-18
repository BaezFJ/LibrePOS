import click


def add_cli_commands(app):
    """Add custom commands to the Flask CLI."""

    from librepos.extensions import db
    from librepos.auth.models import AuthUser

    @app.cli.command("create-bp", help="Create a new blueprint.")
    @click.argument("blueprint_name")
    def create_bp(blueprint_name):
        """Create a new blueprint package directory with standard files."""
        import os
        import re

        if not re.match("^[a-z][a-z0-9_]*$", blueprint_name):
            click.echo(
                "Error: Blueprint name must be lowercase, start with a letter, and contain only letters, numbers, and underscores."
            )
            return

        bp_dir = os.path.join("librepos", blueprint_name)
        if os.path.exists(bp_dir):
            click.echo(f"Error: Blueprint '{blueprint_name}' already exists.")
            return

        # Create a blueprint directory and __init__.py
        os.makedirs(bp_dir)
        open(os.path.join(bp_dir, "__init__.py"), "w").close()

        # Create standard blueprint files
        standard_files = [
            "forms.py",
            "models.py",
            "routes.py",
            "views.py",
        ]
        for file in standard_files:
            with open(os.path.join(bp_dir, file), "w") as f:
                f.write(f"# {blueprint_name} {file[:-3]} module\n")

        # Create templates directory structure
        templates_dir = os.path.join(bp_dir, "templates", blueprint_name)
        os.makedirs(templates_dir)

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
        # from librepos.auth.models import AuthGroup

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

        AuthUser.create(
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
    def create_test_users():
        """Create test users with different roles (superuser, admin, staff, customer)."""
        click.echo("Creating test users...")

        test_users = [
            {
                "username": "owner",
                "email": "owner@test.com",
                "password": "owner123",
                "first_name": "Owner",
                "middle_name": "Test",
                "last_name": "User",
                "role_id": 1,
            },
            {
                "username": "admin",
                "email": "admin@test.com",
                "password": "admin123",
                "first_name": "Admin",
                "middle_name": "Test",
                "last_name": "User",
                "role_id": 2,
            },
            {
                "username": "manager",
                "email": "manager@test.com",
                "password": "manager123",
                "first_name": "Manager",
                "middle_name": "Test",
                "last_name": "User",
                "role_id": 3,
            },
            {
                "username": "cashier",
                "email": "cashier@test.com",
                "password": "cashier123",
                "first_name": "Cashier",
                "middle_name": "Test",
                "last_name": "User",
                "role_id": 4,
            },
            {
                "username": "waiter",
                "email": "waiter@test.com",
                "password": "waiter123",
                "first_name": "Waiter",
                "middle_name": "Test",
                "last_name": "User",
                "role_id": 5,
            },
            {
                "username": "customer",
                "email": "customer@test.com",
                "password": "customer123",
                "first_name": "Customer",
                "middle_name": "Test",
                "last_name": "User",
                "role_id": 10,
            },
        ]

        for user_data in test_users:
            username = user_data["username"]
            if AuthUser.query.filter_by(username=username).first():
                click.echo(f"User '{username}' already exists. Skipping...")
                continue

            AuthUser.create(
                username=user_data["username"],
                email=user_data["email"],
                unsecure_password=user_data["password"],
                first_name=user_data["first_name"],
                middle_name=user_data["middle_name"],
                last_name=user_data["last_name"],
                role_id=user_data["role_id"],
            )
            click.echo(f"Created {username} (password: {user_data['password']})")

        click.echo("\nTest users created successfully!")
        click.echo("Note: These users are for development/testing purposes only.")

    @app.cli.command("seed-role-permissions", help="Seed role permissions from config.")
    def seed_role_permissions():
        """Seed the role_permissions table with data from ROLE_PERMISSIONS config."""
        from librepos.auth.models import AuthRole, AuthPermission, AuthRolePermission
        from librepos.auth.config import ROLE_PERMISSIONS

        click.echo("Seeding role permissions...")

        seeded_count = 0
        skipped_count = 0

        for role_name, permission_names in ROLE_PERMISSIONS.items():
            role = AuthRole.get_first_by(name=role_name)
            if not role:
                click.echo(f"Warning: Role '{role_name}' not found. Skipping...")
                continue

            for permission_name in permission_names:
                permission = AuthPermission.get_first_by(name=permission_name)
                if not permission:
                    click.echo(f"Warning: Permission '{permission_name}' not found. Skipping...")
                    continue

                # Check if the role-permission relationship already exists
                existing = AuthRolePermission.get_first_by(
                    role_id=role.id, permission_id=permission.id
                )

                if existing:
                    skipped_count += 1
                    continue

                AuthRolePermission.create(role_id=role.id, permission_id=permission.id)
                seeded_count += 1

        click.echo("\nRole permissions seeded successfully!")
        click.echo(f"Created: {seeded_count}")
        click.echo(f"Skipped (already exist): {skipped_count}")

    @app.cli.command("reset-db", help="Reset the database.")
    def reset_db():
        """Reset the database."""
        db.drop_all()
        db.create_all()
        click.echo("Done!")
