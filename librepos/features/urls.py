from .main.urls import main_bp
from .branches.routes import branch_bp
from .iam.routes import iam_bp
from .menu.routes import menu_bp
from .orders.routes import order_bp
from .settings.routes import settings_bp

def urlpatterns(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(iam_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(branch_bp)