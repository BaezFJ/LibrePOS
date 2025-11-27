import click


def add_cli_commands(app):
    """Add custom commands to the Flask CLI."""

    from librepos.core.extensions import db
    from librepos.features.iam.models import IAMUser, IAMUserProfile

    @app.cli.command("seed-db", help="Seed the database with data.")
    def seed_db():
        """Seed the database."""
        from .seed_db import seed_all

        click.echo("Seeding the database...")
        seed_all()
        click.echo("Done!")

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
    @click.option("--first-name", prompt=True, help="The first name.", required=True)
    @click.option("--last-name", prompt=True, help="The last name.", required=True)
    @click.option("--email", prompt=True, help="The email address.")
    def add_superuser(username, password, first_name, last_name, email):
        """Add a superuser."""

        click.echo("\nPlease confirm the following details:")
        click.echo(f"Username: {username}")
        click.echo(f"Password: {'*' * len(password)}")
        click.echo(f"First Name: {first_name if first_name else '<empty>'}")
        click.echo(f"Last Name: {last_name if last_name else '<empty>'}")
        click.echo(f"Email: {email if email else '<empty>'}")

        if not click.confirm("\nDo you want to create this superuser?"):
            click.echo("Operation cancelled.")
            return

        user = IAMUser(
            username=username,
            password=password,
            is_superuser=True,
        )
        db.session.add(user)
        db.session.commit()

        profile = IAMUserProfile(
            user_id=user.id, first_name=first_name, last_name=last_name, email=email
        )
        db.session.add(profile)
        db.session.commit()

        click.echo(f"Superuser '{username}' created successfully.")

    @app.cli.command("reset-db", help="Reset the database.")
    def reset_db():
        """Reset the database."""
        db.drop_all()
        db.create_all()
        click.echo("Done!")
