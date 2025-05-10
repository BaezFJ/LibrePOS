from .auth.controllers import auth_bp
from .user.controllers import user_bp

blueprints = [auth_bp, user_bp]
