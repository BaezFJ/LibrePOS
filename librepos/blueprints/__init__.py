from .user.routes import user_bp
from .auth.routes import auth_bp


blueprints = [user_bp, auth_bp]
