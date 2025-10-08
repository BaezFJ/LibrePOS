from flask import Blueprint
# from .auth_routes import auth_bp
# from .role_routes import role_bp
from .user_routes import user_bp

iam_bp = Blueprint("iam", __name__, template_folder="../templates")

# Subdirectories
iam_bp.register_blueprint(user_bp)
# iam_bp.register_blueprint(role_bp)
# iam_bp.register_blueprint(auth_bp)
