from flask import Blueprint, render_template, url_for

from librepos.utils.decorators import permission_required
from .auth_routes import auth_bp
from .policy_routes import policy_bp
from .role_routes import role_bp
from .user_routes import user_bp

iam_bp = Blueprint("iam", __name__, template_folder="../templates", url_prefix="/iam")

# Subdirectories
iam_bp.register_blueprint(user_bp)
iam_bp.register_blueprint(role_bp)
iam_bp.register_blueprint(policy_bp)
iam_bp.register_blueprint(auth_bp)


@iam_bp.get("/")
@iam_bp.get("/home")
@permission_required("iam.allow.access")
def home():
    """Render the IAM home page."""

    context = {
        "title": "IAM",
        "back_url": url_for("settings.home"),
    }
    return render_template("iam/home.html", **context)
