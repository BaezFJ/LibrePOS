import click


def add_cli_commands(app):
    """Add custom commands to the Flask CLI."""

    from librepos.main.extensions import db
    from librepos.features.iam.models import IAMUser, IAMUserProfile

    @app.cli.command("seed-db", help="Seed the database with data.")
    def seed_db():
        """Seed the database."""
        from .seed_db import seed_all

        click.echo("Seeding the database...")
        seed_all()
        click.echo("Done!")

    @app.cli.command("add-superuser", help="Add a superuser.")
    @click.option("--username", prompt=True, help="The username.")
    @click.option(
        "--password",
        prompt=True,
        hide_input=True,
        confirmation_prompt=True,
        help="The password.",
    )
    @click.option("--first-name", prompt=True, help="The first name.")
    @click.option("--last-name", prompt=True, help="The last name.")
    @click.option("--email", prompt=True, help="The email address.")
    def add_superuser(username, password, first_name, last_name, email):
        """Add a superuser."""
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
