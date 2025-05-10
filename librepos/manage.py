import click

from librepos.data.init_data import seed_all


def add_cli_commands(app):
    """Add custom commands to the Flask CLI."""

    from librepos.extensions import db

    @app.cli.command("dev", help="Development commands.")
    @click.option("--reset-db", is_flag=True, help="Reset the database.")
    @click.option("--seed-db", is_flag=True, help="Populate database with sample data.")
    def dev(reset_db=False, seed_db=False):
        """Development commands."""
        if reset_db:
            click.echo("Resetting the database...")
            db.drop_all()
            db.create_all()
            click.echo("Done!")

        if seed_db:
            click.echo("Populating database with sample data...")

            seed_all()

            click.echo("Done!")

    app.cli.add_command(dev)
