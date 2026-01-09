"""Blueprint registration for LibrePOS."""

from .menu import bp as menu_bp


def register_blueprints(app):
    """Register all blueprints with the application.

    Blueprints are imported and registered here. The create_blueprint.py script
    will automatically add new blueprints to this function.
    """
    app.register_blueprint(menu_bp)
