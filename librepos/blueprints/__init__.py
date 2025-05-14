from .auth.controllers import auth_bp
from .users.controllers import user_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")
