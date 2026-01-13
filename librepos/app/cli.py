"""Flask CLI commands for LibrePOS."""

import click
from flask import Flask

from librepos.app.blueprints.menu.models import Category

CATEGORY_SEED_DATA = [
    {
        "name": "Appetizers",
        "description": "Start your meal with our delicious starters",
        "display_order": 1,
    },
    {
        "name": "Soups & Salads",
        "description": "Fresh salads and homemade soups",
        "display_order": 2,
    },
    {"name": "Entrees", "description": "Main course dishes", "display_order": 3},
    {"name": "Sandwiches", "description": "Handcrafted sandwiches and wraps", "display_order": 4},
    {"name": "Pizza", "description": "Artisan pizzas made to order", "display_order": 5},
    {"name": "Sides", "description": "Perfect accompaniments", "display_order": 6},
    {"name": "Desserts", "description": "Sweet treats to finish your meal", "display_order": 7},
    {"name": "Beverages", "description": "Drinks and refreshments", "display_order": 8},
    {"name": "Kids Menu", "description": "Meals for our younger guests", "display_order": 9},
    {"name": "Specials", "description": "Chef's daily specials", "display_order": 10},
]


def register_cli(app: Flask) -> None:
    """Register CLI commands with the Flask app."""

    @app.cli.group()
    def seed():
        """Seed database with sample data."""

    @seed.command("categories")
    def seed_categories():
        """Seed menu categories."""
        created = 0
        skipped = 0

        for data in CATEGORY_SEED_DATA:
            existing = Category.get_first_by(name=data["name"])
            if existing:
                click.echo(f"  Skipped: {data['name']} (already exists)")
                skipped += 1
            else:
                Category.create(**data)
                click.echo(f"  Created: {data['name']}")
                created += 1

        click.echo(f"\nDone! Created: {created}, Skipped: {skipped}")

    @seed.command("all")
    def seed_all():
        """Seed all sample data."""
        click.echo("Seeding categories...")
        ctx = click.get_current_context()
        ctx.invoke(seed_categories)
        # Add more seed commands here as needed
