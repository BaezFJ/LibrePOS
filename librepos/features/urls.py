from .core.routes import core_bp
from .error.routes import error_bp

# from .iam.urls import iam_bp
from .iam.routes import iam_bp
from .auth.routes import auth_bp


def urlpatterns(app):
    app.register_blueprint(error_bp)
    app.register_blueprint(core_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(iam_bp, url_prefix="/iam")
