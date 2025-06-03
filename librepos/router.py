from librepos.main.routes import main_bp
from librepos.auth.routes import auth_bp
from librepos.user.routes import users_bp
from librepos.menu.routes import menu_bp
from librepos.order.routes import order_bp


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(order_bp)
