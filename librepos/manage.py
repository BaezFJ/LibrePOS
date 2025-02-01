import click

from .data.init_data import ROLES, PERMISSIONS
from .models.permission import Permission
from .models.role import Role
from .models.role_permission import RolePermission
from .models.user import User


def add_cli_commands(app):
    """Add custom commands to the Flask CLI."""

    from librepos.extensions import db

    def populate_table(table, data):
        for item in data:
            table.create(**item)

    @app.cli.command("initdb", help="Initialize the database.")
    @click.option("--populate", is_flag=True, help="Populate database with sample data.")
    @click.confirmation_option(prompt="This will drop existing data. Do you want to continue?",
                               help="Initialize the database.")
    def init(populate):
        """Initialize the database."""
        click.echo("Initializing the database...")
        db.drop_all()
        db.create_all()

        populate_table(Permission, PERMISSIONS)
        populate_table(Role, ROLES)

        # Add all permissions to default admin role
        admin_role = Role.query.filter_by(name="admin").first()
        for permission in Permission.query.all():
            RolePermission.create(role_id=admin_role.id, permission_id=permission.id, assigned_by_id=0)

        # Create default admin user
        user_exists = User.query.filter_by(username="admin").first()
        if not user_exists:
            User.create(role_id=admin_role.id, username="admin", password_hash="librepos", first_name="librepos",
                        last_name="forever",
                        email="info@librepos.com")

        click.echo("Done!")

    app.cli.add_command(init)
