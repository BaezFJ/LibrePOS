from .user.routes import user_bp

from .dashboard.routes import dashboard_bp


blueprints = [user_bp, dashboard_bp]
