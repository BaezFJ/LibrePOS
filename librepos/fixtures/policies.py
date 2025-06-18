"""Policies definitions for database seeding."""

# Modular policies based on functional areas
# Each policy groups related permissions for specific management areas

# ======================================================================================================================
#                                           USER MANAGEMENT POLICIES
# ======================================================================================================================
USER_MANAGEMENT_FULL_POLICY = [
    "user.create",
    "user.read",
    "user.list",
    "user.update",
    "user.delete",
]

USER_MANAGEMENT_LIMITED_POLICY = [
    "user.read",
    "user.list",
    "user.update",
]

USER_MANAGEMENT_VIEW_ONLY_POLICY = [
    "user.read",
    "user.list",
]

USER_SELF_MANAGEMENT_POLICY = [
    "user.update.own",
]

# ======================================================================================================================
#                                           ROLE MANAGEMENT POLICIES
# ======================================================================================================================
ROLE_MANAGEMENT_FULL_POLICY = [
    "role.create",
    "role.read",
    "role.list",
    "role.update",
    "role.delete",
]

ROLE_MANAGEMENT_LIMITED_POLICY = [
    "role.read",
    "role.list",
    "role.update",
]

ROLE_MANAGEMENT_VIEW_ONLY_POLICY = [
    "role.read",
    "role.list",
]
# ======================================================================================================================
#                                      ROLE POLICIES MANAGEMENT POLICIES
# ======================================================================================================================
ROLE_POLICIES_FULL_POLICY = [
    "role_policies.read",
    "role_policies.list",
    "role_policies.update",
    "role_policies.create",
    "role_policies.delete",
]

ROLE_POLICIES_LIMITED_POLICY = [
    "role_policies.read",
    "role_policies.list",
    "role_policies.update",
]

ROLE_POLICIES_VIEW_ONLY_POLICY = [
    "role_policies.read",
    "role_policies.list",
]

# ======================================================================================================================
#                                      MENU CATEGORY MANAGEMENT POLICIES
# ======================================================================================================================
MENU_CATEGORY_MANAGEMENT_FULL_POLICY = [
    "menu_category.create",
    "menu_category.read",
    "menu_category.list",
    "menu_category.update",
    "menu_category.delete",
]

MENU_CATEGORY_MANAGEMENT_LIMITED_POLICY = [
    "menu_category.read",
    "menu_category.list",
    "menu_category.update",
]

MENU_CATEGORY_VIEW_ONLY_POLICY = [
    "menu_category.read",
    "menu_category.list",
]

# ======================================================================================================================
#                                      MENU GROUP MANAGEMENT POLICIES
# ======================================================================================================================
MENU_GROUP_MANAGEMENT_FULL_POLICY = [
    "menu_group.create",
    "menu_group.read",
    "menu_group.list",
    "menu_group.update",
    "menu_group.delete",
]

MENU_GROUP_MANAGEMENT_LIMITED_POLICY = [
    "menu_group.read",
    "menu_group.list",
    "menu_group.update",
]

MENU_GROUP_VIEW_ONLY_POLICY = [
    "menu_group.read",
    "menu_group.list",
]

# ======================================================================================================================
#                                      MENU ITEM MANAGEMENT POLICIES
# ======================================================================================================================
MENU_ITEM_MANAGEMENT_FULL_POLICY = [
    "menu_item.create",
    "menu_item.read",
    "menu_item.list",
    "menu_item.update",
    "menu_item.delete",
]

MENU_ITEM_MANAGEMENT_LIMITED_POLICY = [
    "menu_item.read",
    "menu_item.list",
    "menu_item.update",
]

MENU_ITEM_VIEW_ONLY_POLICY = [
    "menu_item.read",
    "menu_item.list",
]

# ======================================================================================================================
#                                      ORDER MANAGEMENT POLICIES
# ======================================================================================================================
ORDER_MANAGEMENT_FULL_POLICY = [
    "order.create",
    "order.read",
    "order.list",
    "order.update",
    "order.void",
    "order.delete",
]

ORDER_MANAGEMENT_OPERATIONAL_POLICY = [
    "order.create",
    "order.read",
    "order.list",
    "order.update",
    "order.void",
]

ORDER_MANAGEMENT_LIMITED_POLICY = [
    "order.create",
    "order.read",
    "order.list",
    "order.update",
]

ORDER_VIEW_ONLY_POLICY = [
    "order.read",
    "order.list",
]
# ======================================================================================================================
#                                      POLICY POLICIES
# ======================================================================================================================
POLICIES_FULL_POLICY = [
    "policy.create",
    "policy.read",
    "policy.list",
    "policy.update",
    "policy.delete",
]

POLICIES_LIMITED_POLICY = [
    "policy.read",
    "policy.list",
    "policy.update",
]

POLICIES_VIEW_ONLY_POLICY = [
    "policy.read",
    "policy.list",
]

# ======================================================================================================================
#                                      SETTINGS MANAGEMENT POLICIES
# ======================================================================================================================
SYSTEM_SETTINGS_FULL_POLICY = [
    "settings.read",
    "system_settings.read",
    "system_settings.update",
    "settings_permissions.read",
]

RESTAURANT_SETTINGS_FULL_POLICY = [
    "settings.read",
    "restaurant.read",
    "restaurant.update",
]

RESTAURANT_SETTINGS_VIEW_ONLY_POLICY = [
    "settings.read",
    "restaurant.read",
]

BASIC_SETTINGS_VIEW_POLICY = [
    "settings.read",
]

# Complete policy definitions with metadata
POLICIES_FIXTURE = [
    # User Management Policies
    (
        "user_management_full",
        "Complete user account management including creation and deletion",
        USER_MANAGEMENT_FULL_POLICY,
    ),
    (
        "user_management_limited",
        "User account management without creation and deletion capabilities",
        USER_MANAGEMENT_LIMITED_POLICY,
    ),
    (
        "user_management_view_only",
        "Read-only access to user account information",
        USER_MANAGEMENT_VIEW_ONLY_POLICY,
    ),
    (
        "user_self_management",
        "Permission to manage own user profile only",
        USER_SELF_MANAGEMENT_POLICY,
    ),
    # Role Management Policies
    (
        "role_management_full",
        "Complete role and permission management capabilities",
        ROLE_MANAGEMENT_FULL_POLICY,
    ),
    (
        "role_management_limited",
        "Role and permission management without creation and deletion capabilities",
        ROLE_MANAGEMENT_LIMITED_POLICY,
    ),
    (
        "role_management_view_only",
        "Read-only access to role and permission information",
        ROLE_MANAGEMENT_VIEW_ONLY_POLICY,
    ),
    # Role Policies Management Policies
    (
        "role_policies_full",
        "Complete role-related permission management",
        ROLE_POLICIES_FULL_POLICY,
    ),
    (
        "role_policies_limited",
        "Role-related permission management without creation and deletion",
        ROLE_POLICIES_LIMITED_POLICY,
    ),
    (
        "role_policies_view_only",
        "Read-only access to role-related permission information",
        ROLE_POLICIES_VIEW_ONLY_POLICY,
    ),
    # Menu Category Management Policies
    (
        "menu_category_management_full",
        "Complete menu category management including creation and deletion",
        MENU_CATEGORY_MANAGEMENT_FULL_POLICY,
    ),
    (
        "menu_category_management_limited",
        "Menu category management without creation and deletion",
        MENU_CATEGORY_MANAGEMENT_LIMITED_POLICY,
    ),
    (
        "menu_category_view_only",
        "Read-only access to menu category information",
        MENU_CATEGORY_VIEW_ONLY_POLICY,
    ),
    # Menu Group Management Policies
    (
        "menu_group_management_full",
        "Complete menu group management including creation and deletion",
        MENU_GROUP_MANAGEMENT_FULL_POLICY,
    ),
    (
        "menu_group_management_limited",
        "Menu group management without creation and deletion",
        MENU_GROUP_MANAGEMENT_LIMITED_POLICY,
    ),
    (
        "menu_group_view_only",
        "Read-only access to menu group information",
        MENU_GROUP_VIEW_ONLY_POLICY,
    ),
    # Menu Item Management Policies
    (
        "menu_item_management_full",
        "Complete menu item management including creation and deletion",
        MENU_ITEM_MANAGEMENT_FULL_POLICY,
    ),
    (
        "menu_item_management_limited",
        "Menu item management without creation and deletion",
        MENU_ITEM_MANAGEMENT_LIMITED_POLICY,
    ),
    (
        "menu_item_view_only",
        "Read-only access to menu item information",
        MENU_ITEM_VIEW_ONLY_POLICY,
    ),
    # Order Management Policies
    (
        "order_management_full",
        "Complete order management including deletion capabilities",
        ORDER_MANAGEMENT_FULL_POLICY,
    ),
    (
        "order_management_operational",
        "Operational order management including void but not delete",
        ORDER_MANAGEMENT_OPERATIONAL_POLICY,
    ),
    (
        "order_management_limited",
        "Basic order processing without void or delete capabilities",
        ORDER_MANAGEMENT_LIMITED_POLICY,
    ),
    (
        "order_view_only",
        "Read-only access to order information",
        ORDER_VIEW_ONLY_POLICY,
    ),
    # Settings Management Policies
    (
        "system_settings_full",
        "Complete system configuration and settings management",
        SYSTEM_SETTINGS_FULL_POLICY,
    ),
    (
        "restaurant_settings_full",
        "Complete restaurant profile and operational settings management",
        RESTAURANT_SETTINGS_FULL_POLICY,
    ),
    (
        "restaurant_settings_view_only",
        "Read-only access to restaurant settings and profile",
        RESTAURANT_SETTINGS_VIEW_ONLY_POLICY,
    ),
    (
        "basic_settings_view",
        "Basic read access to general application settings",
        BASIC_SETTINGS_VIEW_POLICY,
    ),
    # Policy policies
    (
        "policy_policies_full",
        "Complete policy-related permission management",
        POLICIES_FULL_POLICY,
    ),
    (
        "policy_policies_limited",
        "Policy-related permission management without creation and deletion",
        POLICIES_LIMITED_POLICY,
    ),
    (
        "policy_policies_view_only",
        "Read-only access to policy-related permission information",
        POLICIES_VIEW_ONLY_POLICY,
    )
]
