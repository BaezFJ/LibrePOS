import click


def add_cli_commands(app):
    """Add custom commands to the Flask CLI."""

    from librepos.main.extensions import db
    from librepos.features.iam.models import IAMUser

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
    @click.option("--email", prompt=True, help="The email address.")
    def add_superuser(username, password, email):
        """Add a superuser."""
        user = IAMUser(
            username=username,
            password=password,
            email=email,
            is_admin=True,
            is_superuser=True,
        )
        db.session.add(user)
        db.session.commit()
        click.echo(f"Superuser '{username}' created successfully.")

    @app.cli.command("reset-db", help="Reset the database.")
    def reset_db():
        """Reset the database."""
        db.drop_all()
        db.create_all()
        click.echo("Done!")
