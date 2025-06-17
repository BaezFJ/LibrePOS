"""Permission definitions for database seeding."""

# Format: resource.action[.scope]
# Examples:
#   user.update      - Update any user profile
#   user.update.own  - Update only own profile
#   menu_item.create        - Create menu items

USER_PERMISSIONS = [
    (
        "user.create",
        "Create new user accounts with username, email, role assignments and permission settings",
    ),
    (
        "user.read",
        "View detailed user information including profile, roles, and assigned permissions",
    ),
    (
        "user.list",
        "Access and view the complete list of system users with their assigned roles",
    ),
    (
        "user.update",
        "Modify existing user accounts including username, email, role assignments and permissions",
    ),
    ("user.update.own", "Modify own user profile and permissions"),
    ("user.delete", "Permanently remove user accounts from the system"),
]

MENU_CATEGORY_PERMISSIONS = [
    ("menu_category.create", "Create new menu categories for organizing menu items"),
    ("menu_category.read", "View detailed information about specific menu categories"),
    ("menu_category.list", "Access and view the complete list of menu categories"),
    ("menu_category.update", "Modify existing menu category details and properties"),
    ("menu_category.delete", "Remove menu categories from the system"),
]

MENU_GROUP_PERMISSIONS = [
    ("menu_group.create", "Create new menu groups for organizing related menu items"),
    ("menu_group.read", "View detailed information about specific menu groups"),
    ("menu_group.list", "Access and view the complete list of menu groups"),
    ("menu_group.update", "Modify existing menu group details and properties"),
    ("menu_group.delete", "Remove menu groups from the system"),
]

MENU_ITEM_PERMISSIONS = [
    (
        "menu_item.create",
        "Create new menu items with names, prices, and other properties",
    ),
    ("menu_item.read", "View detailed information about specific menu items"),
    ("menu_item.list", "Access and view the complete list of menu items"),
    ("menu_item.update", "Modify existing menu item details, prices, and properties"),
    ("menu_item.delete", "Remove menu items from the system"),
]

POLICY_PERMISSIONS = [
    ("policy.create", "Create new policies with assigned permissions"),
    ("policy.read", "View detailed policy information including permissions"),
    ("policy.list", "Access and view the complete list of policies"),
    ("policy.update", "Modify existing policy details and permissions"),
    ("policy.delete", "Remove policies from the system"),
]

ORDER_PERMISSIONS = [
    ("order.create", "Create new customer orders with selected menu items"),
    ("order.read", "View detailed order information including items and status"),
    ("order.list", "Access and view the complete list of orders"),
    ("order.update", "Modify existing order details, items, and properties"),
    ("order.void", "Mark orders as voided while maintaining record"),
    ("order.delete", "Permanently remove orders from the system"),
]

ORDER_ITEM_PERMISSIONS = [
    ("order_item.create", "Add new items to existing orders"),
    ("order_item.read", "View detailed information about specific order items"),
    ("order_item.list", "Access and view all items within an order"),
    ("order_item.update", "Modify order item details, quantities, and prices"),
    ("order_item.void", "Mark individual order items as voided"),
    ("order_item.delete", "Permanently remove items from orders"),
    ("order_item.send_to_prep", "Send order items to kitchen/preparation area"),
    ("order_item.mark_completed", "Mark order items as completed by kitchen"),
]

RESTAURANT_PERMISSIONS = [
    (
        "restaurant.read",
        "View restaurant profile, contact information, and business details",
    ),
    (
        "restaurant.update",
        "Modify restaurant information, operating hours, and business settings",
    ),
    ("restaurant.create", "Create new restaurant profiles and configurations"),
    ("restaurant.delete", "Remove restaurant profiles from the system"),
    ("restaurant.list", "Access and view all restaurant configurations"),
]

SETTINGS_PERMISSIONS = [
    ("settings.read", "Access and view all application configuration settings"),
    ("system_settings.read", "View system-wide configuration and technical settings"),
    (
        "system_settings.update",
        "Modify system-wide configuration, behavior, and technical parameters",
    ),
    ("settings_permissions.read", "View all permission-related settings"),
]

ROLE_PERMISSIONS = [
    ("role.create", "Create new roles with assigned permissions and settings"),
    ("role.read", "View detailed role information including permissions and settings"),
    ("role.list", "Access and view the complete list of roles"),
    ("role.update", "Modify existing role details and permissions"),
    ("role.delete", "Remove roles from the system"),
]

ROLE_POLICIES_PERMISSIONS = [
    ("role_policies.read", "View all role-related permission policies"),
    (
        "role_policies.list",
        "Access and view the complete list of role-related permission policies",
    ),
    ("role_policies.update", "Modify role-related permission policies"),
    ("role_policies.delete", "Remove role-related permission policies"),
    ("role_policies.create", "Create new role-related permission policies"),
]

# Permissions for the Policy Permissions junction table
POLICY_PERMISSION_PERMISSIONS = [
    ("policy_permission.create", "Assign permissions to policies"),
    ("policy_permission.read", "View permission assignments for policies"),
    ("policy_permission.list", "Access and view all policy-permission relationships"),
    ("policy_permission.update", "Modify permission assignments for policies"),
    ("policy_permission.delete", "Remove permission assignments from policies"),
]

# Group all permissions for easy access
ALL_PERMISSION_FIXTURES = [
    USER_PERMISSIONS,
    ROLE_PERMISSIONS,
    MENU_CATEGORY_PERMISSIONS,
    MENU_GROUP_PERMISSIONS,
    MENU_ITEM_PERMISSIONS,
    ORDER_PERMISSIONS,
    ORDER_ITEM_PERMISSIONS,
    RESTAURANT_PERMISSIONS,
    SETTINGS_PERMISSIONS,
    POLICY_PERMISSIONS,
    POLICY_PERMISSION_PERMISSIONS,
    ROLE_POLICIES_PERMISSIONS,
]
