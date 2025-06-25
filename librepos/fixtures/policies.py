"""Policies definitions for database seeding."""

# Modular policies based on functional areas
# Each policy groups related permissions for specific management areas

# ======================================================================================================================
#                                           IAM USER MANAGEMENT POLICIES
# ======================================================================================================================
IAM_USER_MANAGEMENT_FULL_POLICY = [
    "iam.create.user",
    "iam.read.user",
    "iam.list.user",
    "iam.update.user",
    "iam.delete.user",
    "iam.suspend.user",
]

IAM_USER_MANAGEMENT_LIMITED_POLICY = [
    "iam.read.user",
    "iam.list.user",
    "iam.update.user",
]

IAM_USER_MANAGEMENT_VIEW_ONLY_POLICY = [
    "iam.read.user",
    "iam.list.user",
]

IAM_USER_SELF_MANAGEMENT_POLICY = [
    "iam.update.user.own",
]

# ======================================================================================================================
#                                           IAM ROLE MANAGEMENT POLICIES
# ======================================================================================================================
IAM_ROLE_MANAGEMENT_FULL_POLICY = [
    "iam.create.role",
    "iam.read.role",
    "iam.list.roles",
    "iam.update.role",
    "iam.suspend.role",
    "iam.delete.role",
]

IAM_ROLE_MANAGEMENT_LIMITED_POLICY = [
    "iam.read.role",
    "iam.list.roles",
    "iam.update.role",
]

IAM_ROLE_MANAGEMENT_VIEW_ONLY_POLICY = [
    "iam.read.role",
    "iam.list.roles",
]

# ======================================================================================================================
#                                      IAM POLICY MANAGEMENT POLICIES
# ======================================================================================================================
IAM_POLICY_MANAGEMENT_FULL_POLICY = [
    "iam.create.policy",
    "iam.read.policy",
    "iam.list.policies",
    "iam.update.policy",
    "iam.delete.policy",
]

IAM_POLICY_MANAGEMENT_LIMITED_POLICY = [
    "iam.read.policy",
    "iam.list.policies",
    "iam.update.policy",
]

IAM_POLICY_MANAGEMENT_VIEW_ONLY_POLICY = [
    "iam.read.policy",
    "iam.list.policies",
]

# ======================================================================================================================
#                                      IAM ROLE ASSIGNMENT POLICIES
# ======================================================================================================================
IAM_ROLE_ASSIGNMENT_FULL_POLICY = [
    "iam.assign.policy_to_role",
    "iam.read.role_policies",
    "iam.list.role_policies",
    "iam.update.role_policies",
    "iam.remove.role_policies",
]

IAM_ROLE_ASSIGNMENT_LIMITED_POLICY = [
    "iam.read.role_policies",
    "iam.list.role_policies",
    "iam.update.role_policies",
]

IAM_ROLE_ASSIGNMENT_VIEW_ONLY_POLICY = [
    "iam.read.role_policies",
    "iam.list.role_policies",
]

# ======================================================================================================================
#                                      IAM PERMISSION ASSIGNMENT POLICIES
# ======================================================================================================================
IAM_PERMISSION_ASSIGNMENT_FULL_POLICY = [
    "iam.assign.permission_to_policy",
    "iam.read.policy_permissions",
    "iam.list.policy_permissions",
    "iam.update.policy_permissions",
    "iam.remove.policy_permissions",
]

IAM_PERMISSION_ASSIGNMENT_LIMITED_POLICY = [
    "iam.read.policy_permissions",
    "iam.list.policy_permissions",
    "iam.update.policy_permissions",
]

IAM_PERMISSION_ASSIGNMENT_VIEW_ONLY_POLICY = [
    "iam.read.policy_permissions",
    "iam.list.policy_permissions",
]

# ======================================================================================================================
#                                      MENU CATEGORY MANAGEMENT POLICIES
# ======================================================================================================================
MENU_CATEGORY_MANAGEMENT_FULL_POLICY = [
    "menu.create.category",
    "menu.read.category",
    "menu.list.categories",
    "menu.update.category",
    "menu.delete.category",
]

MENU_CATEGORY_MANAGEMENT_LIMITED_POLICY = [
    "menu.read.category",
    "menu.list.categories",
    "menu.update.category",
]

MENU_CATEGORY_VIEW_ONLY_POLICY = [
    "menu.read.category",
    "menu.list.categories",
]

# ======================================================================================================================
#                                      MENU GROUP MANAGEMENT POLICIES
# ======================================================================================================================
MENU_GROUP_MANAGEMENT_FULL_POLICY = [
    "menu.create.group",
    "menu.read.group",
    "menu.list.groups",
    "menu.update.group",
    "menu.delete.group",
]

MENU_GROUP_MANAGEMENT_LIMITED_POLICY = [
    "menu.read.group",
    "menu.list.groups",
    "menu.update.group",
]

MENU_GROUP_VIEW_ONLY_POLICY = [
    "menu.read.group",
    "menu.list.groups",
]

# ======================================================================================================================
#                                      MENU ITEM MANAGEMENT POLICIES
# ======================================================================================================================
MENU_ITEM_MANAGEMENT_FULL_POLICY = [
    "menu.create.item",
    "menu.read.item",
    "menu.list.items",
    "menu.update.item",
    "menu.delete.item",
]

MENU_ITEM_MANAGEMENT_LIMITED_POLICY = [
    "menu.read.item",
    "menu.list.items",
    "menu.update.item",
]

MENU_ITEM_VIEW_ONLY_POLICY = [
    "menu.read.item",
    "menu.list.items",
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
#                                      ORDER ITEM MANAGEMENT POLICIES
# ======================================================================================================================
ORDER_ITEM_MANAGEMENT_FULL_POLICY = [
    "order.create.item",
    "order.read.item",
    "order.list.items",
    "order.update.item",
    "order.void.item",
    "order.delete.item",
]

ORDER_ITEM_MANAGEMENT_OPERATIONAL_POLICY = [
    "order.create.item",
    "order.read.item",
    "order.list.items",
    "order.update.item",
    "order.void.item",
    "order.send_to_prep",
    "order.mark_completed",
]

ORDER_ITEM_MANAGEMENT_LIMITED_POLICY = [
    "order.create.item",
    "order.read.item",
    "order.list.items",
    "order.update.item",
]

ORDER_ITEM_VIEW_ONLY_POLICY = [
    "order.read.item",
    "order.list.items",
]

# ======================================================================================================================
#                                      RESTAURANT MANAGEMENT POLICIES
# ======================================================================================================================
RESTAURANT_MANAGEMENT_FULL_POLICY = [
    "restaurant.create",
    "restaurant.read",
    "restaurant.list",
    "restaurant.update",
    "restaurant.delete",
]

RESTAURANT_MANAGEMENT_LIMITED_POLICY = [
    "restaurant.read",
    "restaurant.list",
    "restaurant.update",
]

RESTAURANT_MANAGEMENT_VIEW_ONLY_POLICY = [
    "restaurant.read",
    "restaurant.list",
]

# ======================================================================================================================
#                                      SETTINGS MANAGEMENT POLICIES
# ======================================================================================================================
SYSTEM_SETTINGS_FULL_POLICY = [
    "settings.access",
    "settings.read.system",
    "settings.update.system",
]

SYSTEM_SETTINGS_LIMITED_POLICY = [
    "settings.access",
    "settings.read.system",
]

BASIC_SETTINGS_VIEW_POLICY = [
    "settings.access",
]

# ======================================================================================================================
#                                      IAM ACCESS POLICIES
# ======================================================================================================================
IAM_FULL_ACCESS_POLICY = [
    "iam.access",
    "iam.dashboard",
    "iam.audit",
    "iam.bulk_operations",
    "iam.export",
    "iam.import",
]

IAM_BASIC_ACCESS_POLICY = [
    "iam.access",
    "iam.dashboard",
]

# Complete policy definitions with metadata
POLICIES_FIXTURE = [
    # IAM User Management Policies
    (
        "iam_user_management_full",
        "Complete IAM user account management including creation and deletion",
        IAM_USER_MANAGEMENT_FULL_POLICY,
    ),
    (
        "iam_user_management_limited",
        "IAM user account management without creation and deletion capabilities",
        IAM_USER_MANAGEMENT_LIMITED_POLICY,
    ),
    (
        "iam_user_management_view_only",
        "Read-only access to IAM user account information",
        IAM_USER_MANAGEMENT_VIEW_ONLY_POLICY,
    ),
    (
        "iam_user_self_management",
        "Permission to manage own IAM user profile only",
        IAM_USER_SELF_MANAGEMENT_POLICY,
    ),
    # IAM Role Management Policies
    (
        "iam_role_management_full",
        "Complete IAM role management capabilities",
        IAM_ROLE_MANAGEMENT_FULL_POLICY,
    ),
    (
        "iam_role_management_limited",
        "IAM role management without creation and deletion capabilities",
        IAM_ROLE_MANAGEMENT_LIMITED_POLICY,
    ),
    (
        "iam_role_management_view_only",
        "Read-only access to IAM role information",
        IAM_ROLE_MANAGEMENT_VIEW_ONLY_POLICY,
    ),
    # IAM Policy Management Policies
    (
        "iam_policy_management_full",
        "Complete IAM policy management capabilities",
        IAM_POLICY_MANAGEMENT_FULL_POLICY,
    ),
    (
        "iam_policy_management_limited",
        "IAM policy management without creation and deletion capabilities",
        IAM_POLICY_MANAGEMENT_LIMITED_POLICY,
    ),
    (
        "iam_policy_management_view_only",
        "Read-only access to IAM policy information",
        IAM_POLICY_MANAGEMENT_VIEW_ONLY_POLICY,
    ),
    # IAM Permission Assignment Policies
    (
        "iam_permission_assignment_full",
        "Complete permission assignment management",
        IAM_PERMISSION_ASSIGNMENT_FULL_POLICY,
    ),
    (
        "iam_permission_assignment_limited",
        "Permission assignment management without removal capabilities",
        IAM_PERMISSION_ASSIGNMENT_LIMITED_POLICY,
    ),
    (
        "iam_permission_assignment_view_only",
        "Read-only access to permission assignment information",
        IAM_PERMISSION_ASSIGNMENT_VIEW_ONLY_POLICY,
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
    # Order Item Management Policies
    (
        "order_item_management_full",
        "Complete order item management including deletion capabilities",
        ORDER_ITEM_MANAGEMENT_FULL_POLICY,
    ),
    (
        "order_item_management_operational",
        "Operational order item management including kitchen operations",
        ORDER_ITEM_MANAGEMENT_OPERATIONAL_POLICY,
    ),
    (
        "order_item_management_limited",
        "Basic order item processing without void or delete capabilities",
        ORDER_ITEM_MANAGEMENT_LIMITED_POLICY,
    ),
    (
        "order_item_view_only",
        "Read-only access to order item information",
        ORDER_ITEM_VIEW_ONLY_POLICY,
    ),
    # Restaurant Management Policies
    (
        "restaurant_management_full",
        "Complete restaurant profile and configuration management",
        RESTAURANT_MANAGEMENT_FULL_POLICY,
    ),
    (
        "restaurant_management_limited",
        "Restaurant management without creation and deletion capabilities",
        RESTAURANT_MANAGEMENT_LIMITED_POLICY,
    ),
    (
        "restaurant_management_view_only",
        "Read-only access to restaurant settings and profile",
        RESTAURANT_MANAGEMENT_VIEW_ONLY_POLICY,
    ),
    # Settings Management Policies
    (
        "system_settings_full",
        "Complete system configuration and settings management",
        SYSTEM_SETTINGS_FULL_POLICY,
    ),
    (
        "system_settings_limited",
        "Limited system settings access without modification capabilities",
        SYSTEM_SETTINGS_LIMITED_POLICY,
    ),
    (
        "basic_settings_view",
        "Basic read access to general application settings",
        BASIC_SETTINGS_VIEW_POLICY,
    ),
    # IAM Access Policies
    (
        "iam_full_access",
        "Complete IAM interface access with advanced operations",
        IAM_FULL_ACCESS_POLICY,
    ),
    (
        "iam_basic_access",
        "Basic IAM interface access and dashboard viewing",
        IAM_BASIC_ACCESS_POLICY,
    ),
    # IAM Role Assignment Policies
    (
        "iam_role_assignment_full",
        "Complete role assignment management capabilities",
        IAM_ROLE_ASSIGNMENT_FULL_POLICY,
    ),
    (
        "iam_role_assignment_limited",
        "Role assignment management without removal capabilities",
        IAM_ROLE_ASSIGNMENT_LIMITED_POLICY,
    ),
    (
        "iam_role_assignment_view_only",
        "Read-only access to role assignment information",
        IAM_ROLE_ASSIGNMENT_VIEW_ONLY_POLICY,
    ),
]
