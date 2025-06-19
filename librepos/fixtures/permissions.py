"""Permission definitions for database seeding."""

# Format: domain.action[.scope]
#   domain - The controller, main category or area of functionality
#   action - The specific operation or permission being granted
#   [.scope] - An optional scope or context (indicated by square brackets)
# Examples:
#   user.update      - Update any user profile
#   user.update.own  - Update only own profile
#   menu.create.item - Create menu item

# User Management Domain
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

# Menu Management Domain
MENU_PERMISSIONS = [
    # Categories
    ("menu.create.category", "Create new menu categories for organizing menu items"),
    ("menu.read.category", "View detailed information about specific menu categories"),
    ("menu.list.categories", "Access and view the complete list of menu categories"),
    ("menu.update.category", "Modify existing menu category details and properties"),
    ("menu.delete.category", "Remove menu categories from the system"),
    # Groups
    ("menu.create.group", "Create new menu groups for organizing related menu items"),
    ("menu.read.group", "View detailed information about specific menu groups"),
    ("menu.list.groups", "Access and view the complete list of menu groups"),
    ("menu.update.group", "Modify existing menu group details and properties"),
    ("menu.delete.group", "Remove menu groups from the system"),
    # Items
    (
        "menu.create.item",
        "Create new menu items with names, prices, and other properties",
    ),
    ("menu.read.item", "View detailed information about specific menu items"),
    ("menu.list.items", "Access and view the complete list of menu items"),
    ("menu.update.item", "Modify existing menu item details, prices, and properties"),
    ("menu.delete.item", "Remove menu items from the system"),
]

# Order Management Domain
ORDER_PERMISSIONS = [
    # Orders
    ("order.create", "Create new customer orders with selected menu items"),
    ("order.read", "View detailed order information including items and status"),
    ("order.list", "Access and view the complete list of orders"),
    ("order.update", "Modify existing order details, items, and properties"),
    ("order.void", "Mark orders as voided while maintaining record"),
    ("order.delete", "Permanently remove orders from the system"),
    # Order Items
    ("order.create.item", "Add new items to existing orders"),
    ("order.read.item", "View detailed information about specific order items"),
    ("order.list.items", "Access and view all items within an order"),
    ("order.update.item", "Modify order item details, quantities, and prices"),
    ("order.void.item", "Mark individual order items as voided"),
    ("order.delete.item", "Permanently remove items from orders"),
    ("order.send_to_prep", "Send order items to kitchen/preparation area"),
    ("order.mark_completed", "Mark order items as completed by kitchen"),
]

# Restaurant Management Domain
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

# System Settings Domain
SETTINGS_PERMISSIONS = [
    ("settings.read", "Access and view all application configuration settings"),
    ("settings.read.system", "View system-wide configuration and technical settings"),
    (
        "settings.update.system",
        "Modify system-wide configuration, behavior, and technical parameters",
    ),
    ("settings.read.permissions", "View all permission-related settings"),
]

# IAM (Identity and Access Management) Domain
IAM_PERMISSIONS = [
    # General IAM Access
    ("iam.access", "Access Identity and Access Management interface"),
    ("iam.dashboard", "View IAM dashboard with system overview and statistics"),
    # Role Management
    ("iam.create.role", "Create new roles with assigned permissions and settings"),
    (
        "iam.read.role",
        "View detailed role information including permissions and settings",
    ),
    ("iam.list.roles", "Access and view the complete list of roles"),
    ("iam.update.role", "Modify existing role details and permissions"),
    ("iam.delete.role", "Remove roles from the system"),
    # Policy Management
    ("iam.create.policy", "Create new policies with assigned permissions"),
    ("iam.read.policy", "View detailed policy information including permissions"),
    ("iam.list.policies", "Access and view the complete list of policies"),
    ("iam.update.policy", "Modify existing policy details and permissions"),
    ("iam.delete.policy", "Remove policies from the system"),
    # Policy-Permission Assignments
    ("iam.assign.permissions", "Assign permissions to policies"),
    ("iam.read.assignments", "View permission assignments for policies"),
    ("iam.list.assignments", "Access and view all policy-permission relationships"),
    ("iam.update.assignments", "Modify permission assignments for policies"),
    ("iam.remove.assignments", "Remove permission assignments from policies"),
    # Advanced IAM Operations
    ("iam.audit", "View IAM audit logs and permission changes"),
    ("iam.bulk_operations", "Perform bulk operations on users, roles, and policies"),
    ("iam.export", "Export IAM configurations and reports"),
    ("iam.import", "Import IAM configurations"),
]

# Group all permissions for easy access
ALL_PERMISSION_FIXTURES = [
    USER_PERMISSIONS,
    MENU_PERMISSIONS,
    ORDER_PERMISSIONS,
    RESTAURANT_PERMISSIONS,
    SETTINGS_PERMISSIONS,
    IAM_PERMISSIONS,
]
