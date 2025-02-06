import click

from librepos.blueprints.user.models import Group
from librepos.blueprints.user.models import Permission
from librepos.blueprints.user.models import Policy
from librepos.blueprints.user.models import Role
from librepos.blueprints.user.models import (
    User,
    PermissionPolicy,
    PolicyGroup,
    GroupUser,
)
from .data.init_data import ROLES, PERMISSIONS, POLICIES, GROUPS


def add_cli_commands(app):
    """Add custom commands to the Flask CLI."""

    from librepos.extensions import db

    def populate_table(table, data):
        for item in data:
            table.create(**item)

    @app.cli.command("initdb", help="Initialize the database.")
    @click.option(
        "--populate", is_flag=True, help="Populate database with sample data."
    )
    @click.confirmation_option(
        prompt="This will drop existing data. Do you want to continue?",
        help="Initialize the database.",
    )
    def init(populate):
        """Initialize the database."""
        click.echo("Initializing the database...")
        db.drop_all()
        db.create_all()

        populate_table(Permission, PERMISSIONS)
        populate_table(Policy, POLICIES)
        populate_table(Group, GROUPS)
        populate_table(Role, ROLES)

        # permission_policy
        _permissions = Permission.query.all()
        _administrator_access_policy = Policy.query.filter_by(
            name="AdministratorAccess"
        ).first()

        if _administrator_access_policy:
            for _permission in _permissions:
                PermissionPolicy.create(
                    permission_id=_permission.id,
                    policy_id=_administrator_access_policy.id,
                )

        _administrator_group = Group.query.filter_by(name="Administrator").first()
        if _administrator_group and _administrator_access_policy:
            PolicyGroup.create(
                group_id=_administrator_group.id,
                policy_id=_administrator_access_policy.id,
            )

        # Create default admin
        user_exists = User.query.count()
        admin_role = Role.query.filter_by(name="admin").first()
        
        if not user_exists and admin_role:
            User.create(
                role_id=admin_role.id,
                password="librepos",
                email="admin@librepos.com",
            )

        # add the newly create admin user to the Administrator Group
        admin_group = Group.query.filter_by(name="Administrator").first()
        if admin_group:
            admin_user = User.query.filter_by(email="admin@librepos.com").first()
            if admin_user:
                GroupUser.create(group_id=admin_group.id, user_id=admin_user.id)

        click.echo("Done!")

    app.cli.add_command(init)
