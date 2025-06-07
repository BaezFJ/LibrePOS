from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required

from librepos.auth.decorators import permission_required
from librepos.utils import sanitize_form_data
from librepos.forms import RestaurantForm

from .service import MainService

settings_bp = Blueprint(
    "settings", __name__, template_folder="templates", url_prefix="/settings"
)

main_service = MainService()


@settings_bp.before_request
@login_required
def before_request():
    """Force the user to log in before accessing any page."""
    pass


@settings_bp.get("/")
def index():
    context = {
        "title": "Settings",
    }
    return render_template("settings/index.html", **context)


# ======================================================================================================================
#                                              SYSTEM SETTINGS ROUTES
# ======================================================================================================================
@settings_bp.get("/system-settings")
def system_settings():
    context = {
        "title": "System",
        "back_url": url_for(".index"),
    }
    return render_template("settings/system_settings.html", **context)


# ======================================================================================================================
#                                              RESTAURANT ROUTES
# ======================================================================================================================


# ================================
#            READ
# ================================
@settings_bp.get("/restaurant")
@permission_required("get_restaurant")
def get_restaurant():
    form = RestaurantForm(obj=main_service.get_restaurant())
    context = {
        "title": "Restaurant",
        "back_url": url_for(".settings"),
        "restaurant": main_service.get_restaurant(),
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
        for key, value in sanitized_data.items():
            print(f"key: {key} -> value: {value}")
        main_service.update_restaurant(sanitized_data)
    return redirect(url_for(".settings"))
