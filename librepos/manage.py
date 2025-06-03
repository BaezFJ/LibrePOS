import click

from librepos.seeds import seed_all


def add_cli_commands(app):
    """Add custom commands to the Flask CLI."""

    from librepos.extensions import db

    @app.cli.command("initdb", help="Initialize the database.")
    def initdb():
        """Initialize the database and seed it with data."""
        db.drop_all()
        click.echo("Initializing the database...")
        db.create_all()
        click.echo("Seeding the database...")
        seed_all()
        click.echo("Done!")

    @app.cli.command("dev", help="Development commands.")
    @click.option("--reset-db", is_flag=True, help="Reset the database.")
    def dev(reset_db=False):
        """Development commands."""
        if reset_db:
            click.echo("Resetting the database...")
            db.drop_all()
            db.create_all()
            seed_all()
            click.echo("Done!")

    app.cli.add_command(dev)
    app.cli.add_command(initdb)
