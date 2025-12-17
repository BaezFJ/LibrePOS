from .main.routes import main_bp
from .error.routes import error_bp
from .auth.routes import iam_bp


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(error_bp, url_prefix="/error")
    app.register_blueprint(iam_bp, url_prefix="/auth")
