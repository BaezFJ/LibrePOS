from librepos.controllers.auth_controller import auth_bp
from librepos.controllers.menu_controller import menu_bp
from librepos.controllers.order_controller import order_bp
from librepos.controllers.settings_controller import settings_bp
from librepos.controllers.user_controller import users_bp


def register_blueprints(app):
    app.register_blueprint(settings_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(order_bp)
