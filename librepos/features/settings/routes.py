from flask import Blueprint, render_template, url_for, redirect

from librepos.utils import sanitize_form_data
from librepos.utils.decorators import permission_required
from .forms import SystemSettingsForm
from .services import SystemSettingsService

settings_bp = Blueprint(
    "settings", __name__, template_folder="templates", url_prefix="/settings"
)

system_settings_service = SystemSettingsService()


@settings_bp.get("/")
@permission_required("settings.access")
def home():
    return render_template("settings/home.html", title="Settings")


# ======================================================================================================================
#                                            SYSTEM ROUTES
# ======================================================================================================================


# ================================
#            READ
# ================================
@settings_bp.get("/system")
@permission_required("settings.read.system")
def system_settings():
    """Render the system settings page."""
    settings = system_settings_service.repository.get_by_id(1)
    form = SystemSettingsForm(obj=settings)
    context = {
        "title": "Settings",
        "back_url": url_for(".home"),
        "form": form,
        "settings": settings,
    }
    return render_template("settings/system_settings.html", **context)


# ================================
#            UPDATE
# ================================
@settings_bp.post("/update-system-settings")
@permission_required("settings.update.system")
def update_system_settings():
    form = SystemSettingsForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        system_settings_service.update_system_settings(sanitized_data)
    return redirect(url_for(".system_settings"))
