"""Blueprint registration for LibrePOS."""

from .auth import bp as auth_bp


def register_blueprints(app):
    """Register all blueprints with the application.

    Blueprints are imported and registered here. The create_blueprint.py script
    will automatically add new blueprints to this function.
    """
    app.register_blueprint(auth_bp)
