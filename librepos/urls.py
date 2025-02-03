from librepos.routes.dashboard import dashboard_bp
from librepos.routes.auth import auth_bp


def register_urls(app):
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)
