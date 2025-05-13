from librepos.auth.controllers import auth_bp
from librepos.users.controllers import user_bp


def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")
