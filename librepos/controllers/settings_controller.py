from flask import Blueprint, render_template, url_for, redirect, request, jsonify
from flask_login import login_required

from librepos.forms import RestaurantForm, SystemSettingsForm, RoleForm
from librepos.services import (
    RestaurantService,
    SystemSettingsService,
    PermissionService,
)
from librepos.utils import sanitize_form_data
from librepos.utils.decorators import permission_required

settings_bp = Blueprint(
    "settings", __name__, template_folder="templates", url_prefix="/settings"
)

restaurant_service = RestaurantService()
system_settings_service = SystemSettingsService()
permission_service = PermissionService()

nav_title = "Settings"


@settings_bp.before_request
@login_required
def before_request():
    """Force the user to log in before accessing any page."""
    pass


@settings_bp.get("/")
@permission_required("settings.read")
def index():
    return render_template("settings/index.html", title="Settings")


# ======================================================================================================================
#                                            SYSTEM ROUTES
# ======================================================================================================================


# ================================
#            READ
# ================================
@settings_bp.get("/system")
@permission_required("system_settings.read")
def system_settings():
    """Render the system settings page."""
    settings = system_settings_service.repository.get_by_id(1)
    form = SystemSettingsForm(obj=settings)
    context = {
        "title": nav_title,
        "back_url": url_for(".index"),
        "form": form,
        "settings": settings,
    }
    return render_template("settings/system_settings.html", **context)


# ================================
#            UPDATE
# ================================
@settings_bp.post("/update-system-settings")
@permission_required("system_settings.update")
def update_system_settings():
    form = SystemSettingsForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        system_settings_service.update_system_settings(sanitized_data)
    return redirect(url_for(".system_settings"))


# ======================================================================================================================
#                                            SYSTEM / PERMISSIONS ROUTES
# ======================================================================================================================


# ================================
#            CREATE
# ================================
@settings_bp.post("/create-role")
@permission_required("role.create")
def create_role():
    form = RoleForm()
    if form.validate_on_submit():
        validated_data = sanitize_form_data(form)
        permission_service.create_role(validated_data)
    return redirect(url_for(".list_user_roles"))


# ================================
#            READ
# ================================
@settings_bp.get("/user-roles")
def list_user_roles():
    """Render the user roles page."""
    context = {
        "title": nav_title,
        "back_url": url_for(".index"),
        "roles": permission_service.list_roles(),
        "form": RoleForm(),
    }
    return render_template("settings/list_user_roles.html", **context)


@settings_bp.get("/user-roles/<int:role_id>")
def get_user_role(role_id):
    """Render the user role page."""
    role = permission_service.get_role(role_id)
    unassign_policies = permission_service.list_unassign_policies(role_id)
    form = RoleForm(obj=role)
    context = {
        "title": nav_title,
        "back_url": url_for(".list_user_roles"),
        "role": role,
        "form": form,
        "unassign_policies": unassign_policies,
    }
    return render_template("settings/get_user_role.html", **context)


# ================================
#            UPDATE
# ================================
@settings_bp.post("/user-roles/<int:role_id>/update")
def update_user_role(role_id):
    """Update the user role."""
    form = RoleForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        permission_service.update_role(role_id, sanitized_data)
    return redirect(url_for(".get_user_role", role_id=role_id))


@settings_bp.post("/user-roles/<int:role_id>/update-policies")
def update_user_role_policies(role_id):
    """Update role policies."""
    form_data = request.form.items()
    policies = []

    for item in form_data:
        if item[0].startswith("policy_"):
            policies.append(item[1])

    permission_service.assign_policies(role_id, policies)

    return redirect(url_for(".get_user_role", role_id=role_id))


# ================================
#            DELETE
# ================================
@settings_bp.post("/user-roles/<int:role_id>/unassign-policy/<int:policy_id>")
def remove_role_policy(role_id, policy_id):
    """Update role policies."""
    permission_service.unassign_policy(role_id, policy_id)
    # Return a redirect header HTMX understands
    response = jsonify(success=True)
    response.headers["HX-Redirect"] = url_for(".get_user_role", role_id=role_id)
    return response


# ======================================================================================================================
#                                              RESTAURANT ROUTES
# ======================================================================================================================


# ================================
#            READ
# ================================
@settings_bp.get("/restaurant")
@permission_required("restaurant.read")
def get_restaurant():
    restaurant = restaurant_service.repository.get_by_id(1)
    form = RestaurantForm(obj=restaurant)
    context = {
        "title": nav_title,
        "back_url": url_for(".index"),
        "restaurant": restaurant,
        "form": form,
    }
    return render_template("settings/get_restaurant.html", **context)


# ================================
#            UPDATE
# ================================
@settings_bp.post("/update-restaurant")
@permission_required("restaurant.update")
def update_restaurant():
    form = RestaurantForm()
    if form.validate_on_submit():
        sanitized_data = sanitize_form_data(form)
        restaurant_service.update_restaurant(sanitized_data)
    return redirect(url_for(".get_restaurant"))
