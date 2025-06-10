from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required

from librepos.forms import RestaurantForm, SystemSettingsForm
from librepos.services import RestaurantService, SystemSettingsService
from librepos.utils import sanitize_form_data
from librepos.utils.decorators import permission_required

settings_bp = Blueprint(
    "settings", __name__, template_folder="templates", url_prefix="/settings"
)

restaurant_service = RestaurantService()
system_settings_service = SystemSettingsService()


@settings_bp.before_request
@login_required
def before_request():
    """Force the user to log in before accessing any page."""
    pass


@settings_bp.get("/")
@permission_required("get_settings")
def index():
    return render_template("settings/index.html", title="Settings")


# ======================================================================================================================
#                                            SYSTEM SETTINGS ROUTES
# ======================================================================================================================


# ================================
#            READ
# ================================
@settings_bp.get("/system")
@permission_required("view_system_settings")
def system_settings():
    """Render the system settings page."""
    settings = system_settings_service.repository.get_by_id(1)
    form = SystemSettingsForm(obj=settings)
    context = {
        "title": "System",
        "back_url": url_for(".index"),
        "form": form,
        "settings": settings,
    }
    return render_template("settings/system_settings.html", **context)


# ================================
#            UPDATE
# ================================
@settings_bp.post("/update-system-settings")
@permission_required("update_system_settings")
def update_system_settings():
    form = SystemSettingsForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        system_settings_service.update_system_settings(sanitized_data)
    return redirect(url_for(".system_settings"))


# ======================================================================================================================
#                                              RESTAURANT ROUTES
# ======================================================================================================================


# ================================
#            READ
# ================================
@settings_bp.get("/restaurant")
@permission_required("get_restaurant")
def get_restaurant():
    restaurant = restaurant_service.repository.get_by_id(1)
    form = RestaurantForm(obj=restaurant)
    context = {
        "title": "Restaurant",
        "back_url": url_for(".index"),
        "restaurant": restaurant,
        "form": form,
    }
    return render_template("settings/get_restaurant.html", **context)


# ================================
#            UPDATE
# ================================
@settings_bp.post("/update-restaurant")
@permission_required("update_restaurant")
def update_restaurant():
    form = RestaurantForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        restaurant_service.update_restaurant(sanitized_data)
    return redirect(url_for(".get_restaurant"))
