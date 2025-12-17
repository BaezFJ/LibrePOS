from flask import Blueprint

from . import views

error_bp = Blueprint("error", __name__, template_folder="templates")

error_bp.app_errorhandler(403)(views.access_denied)
error_bp.app_errorhandler(404)(views.page_not_found)
error_bp.app_errorhandler(500)(views.internal_server_error)
