from .main.routes import main_bp
from .branches.routes import branch_bp
from .iam.routes import iam_bp
from .iam.routes.auth_routes import auth_bp
from .menu.routes import menu_bp
from .orders.routes import order_bp
from .settings.routes import settings_bp

def urlpatterns(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(iam_bp, url_prefix="/iam")
    app.register_blueprint(order_bp, url_prefix="/orders")
    app.register_blueprint(menu_bp, url_prefix="/menu")
    app.register_blueprint(settings_bp, url_prefix="/settings")
    app.register_blueprint(branch_bp, url_prefix="/branch")