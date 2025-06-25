from .auth.user_login_form import UserLoginForm
from .common.confirm_deletion_form import ConfirmDeletionForm
from .iam.role_form import RoleForm
from .iam.user_address_form import UserAddressForm
from .iam.user_contact_form import UserContactForm
from .iam.user_creation_form import UserCreationForm
from .iam.user_details_form import UserDetailsForm
from .iam.user_role_form import UserRoleForm
from .menu.menu_category_form import MenuCategoryForm
from .menu.menu_group_form import MenuGroupForm
from .menu.menu_item_form import MenuItemForm
from .settings.restaurant_form import RestaurantForm
from .settings.system_settings_form import SystemSettingsForm

__all__ = [
    "UserCreationForm",
    "UserContactForm",
    "UserAddressForm",
    "UserDetailsForm",
    "UserLoginForm",
    "UserRoleForm",
    "MenuCategoryForm",
    "MenuGroupForm",
    "MenuItemForm",
    "RestaurantForm",
    "SystemSettingsForm",
    "RoleForm",
    "ConfirmDeletionForm",
]
