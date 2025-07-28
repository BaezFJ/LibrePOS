from librepos.features.branches.utils.enums import BranchPermissions
from librepos.features.iam.utils.enums import IAMPermissions
from librepos.features.menu.utils.enums import MenuPermissions
from librepos.features.orders.utils.enums import OrderPermissions
from librepos.features.settings.utils.enums import SettingsPermissions

iam_permissions_list = [
    (
        IAMPermissions.ACCESS,
        "View and navigate the Identity and Access Management (IAMPermissions) interface for managing users, roles and permissions",
    ),
    (
        IAMPermissions.CREATE_USER,
        "Create new user accounts and assign them specific roles and permissions for system access",
    ),
    (
        IAMPermissions.READ_USER,
        "View complete user profile information including assigned roles, permissions and account details",
    ),
    (
        IAMPermissions.LIST_USER,
        "View and search through the complete list of system users with their assigned roles and status",
    ),
    (
        IAMPermissions.UPDATE_USER,
        "Modify existing user profiles including roles, permissions, contact information and account status",
    ),
    (
        IAMPermissions.DELETE_USER,
        "Permanently remove user accounts and revoke all associated system access privileges",
    ),
    (
        IAMPermissions.CREATE_ROLE,
        "Define new roles with specific sets of permissions that can be assigned to multiple users",
    ),
    (
        IAMPermissions.READ_ROLE,
        "View detailed role configurations including all associated permissions and access levels",
    ),
    (
        IAMPermissions.LIST_ROLE,
        "View and search through all system roles and their assigned permissions and user assignments",
    ),
    (
        IAMPermissions.UPDATE_ROLE,
        "Modify existing role configurations including adding/removing permissions and access levels",
    ),
    (
        IAMPermissions.DELETE_ROLE,
        "Permanently remove roles from the system and unassign them from all associated users",
    ),
    (
        IAMPermissions.CREATE_POLICY,
        "Define new policies with specific sets of permissions",
    ),
    (
        IAMPermissions.READ_POLICY,
        "View detailed policy configurations and permission sets defined in the system",
    ),
    (
        IAMPermissions.LIST_POLICY,
        "View and search through all system policies and their associated permissions",
    ),
    (
        IAMPermissions.UPDATE_POLICY,
        "Modify existing policy configurations including permission sets",
    ),
    (
        IAMPermissions.DELETE_POLICY,
        "Permanently remove policies from the system excluding system defaults.",
    ),
]

menu_permissions = [
    (
        MenuPermissions.ACCESS,
        "View and navigate the Menu Management interface for configuring restaurant menus",
    ),
    (
        MenuPermissions.CREATE_CATEGORY,
        "Create new menu categories to organize menu items (e.g. Appetizers, Entrees)",
    ),
    (
        MenuPermissions.READ_CATEGORY,
        "View detailed menu category information including description and contained items",
    ),
    (
        MenuPermissions.LIST_CATEGORY,
        "View and search through all menu categories and their organizational structure",
    ),
    (
        MenuPermissions.UPDATE_CATEGORY,
        "Modify existing menu category details including name, description and organization",
    ),
    (
        MenuPermissions.DELETE_CATEGORY,
        "Permanently remove menu categories and reassign or delete contained items",
    ),
    (
        MenuPermissions.CREATE_GROUP,
        "Create new menu groups within categories for further menu organization",
    ),
    (
        MenuPermissions.READ_GROUP,
        "View detailed menu group information including contained items and category assignment",
    ),
    (
        MenuPermissions.LIST_GROUP,
        "View and search through all menu groups and their organizational structure",
    ),
    (
        MenuPermissions.UPDATE_GROUP,
        "Modify existing menu group details including name, category and organization",
    ),
    (
        MenuPermissions.DELETE_GROUP,
        "Permanently remove menu groups and reassign or delete contained items",
    ),
    (
        MenuPermissions.CREATE_ITEM,
        "Add new menu items with pricing, descriptions and category/group assignments",
    ),
    (
        MenuPermissions.READ_ITEM,
        "View detailed menu item information including pricing, descriptions and availability",
    ),
    (
        MenuPermissions.LIST_ITEM,
        "View and search through all menu items across categories and groups",
    ),
    (
        MenuPermissions.UPDATE_ITEM,
        "Modify existing menu item details including pricing, descriptions and assignments",
    ),
    (MenuPermissions.DELETE_ITEM, "Permanently remove menu items from the system"),
]

order_permissions = [
    (
        OrderPermissions.ACCESS,
        "View and navigate the Order Management interface for processing customer orders",
    ),
    (
        OrderPermissions.CREATE_TICKET,
        "Create new order tickets with customer and table information",
    ),
    (
        OrderPermissions.READ_TICKET,
        "View detailed order ticket information including items, status and payment details",
    ),
    (
        OrderPermissions.LIST_TICKET,
        "View and search through all order tickets with their current status",
    ),
    (
        OrderPermissions.UPDATE_TICKET,
        "Modify existing order ticket details including status, items and payment information",
    ),
    (
        OrderPermissions.DELETE_TICKET,
        "Permanently remove order tickets from the system",
    ),
    (
        OrderPermissions.CREATE_TICKET_ITEM,
        "Add individual menu items to order tickets with quantity and special instructions",
    ),
    (
        OrderPermissions.READ_TICKET_ITEM,
        "View detailed order item information including modifiers and preparation status",
    ),
    (
        OrderPermissions.LIST_TICKET_ITEM,
        "View all items across order tickets with their current status",
    ),
    (
        OrderPermissions.UPDATE_TICKET_ITEM,
        "Modify ordered items including quantity, special instructions and preparation status",
    ),
    (OrderPermissions.DELETE_TICKET_ITEM, "Remove individual items from order tickets"),
]

branch_permissions = [
    (
        BranchPermissions.ACCESS,
        "View and navigate the Branch Management interface for multiple location management",
    ),
    (
        BranchPermissions.CREATE_BRANCH,
        "Create new branch locations with address and contact information",
    ),
    (
        BranchPermissions.READ_BRANCH,
        "View detailed branch information including location, staff and operational details",
    ),
    (
        BranchPermissions.LIST_BRANCH,
        "View and search through all branch locations with their current status",
    ),
    (
        BranchPermissions.UPDATE_BRANCH,
        "Modify existing branch details including location, contact info and operational settings",
    ),
    (
        BranchPermissions.DELETE_BRANCH,
        "Permanently remove branch locations from the system",
    ),
]

settings_permissions = [
    (
        SettingsPermissions.ACCESS,
        "View and navigate the System Settings interface for global configuration",
    ),
    (
        SettingsPermissions.LIST_SETTINGS,
        "View and search through all system configuration settings",
    ),
    (
        SettingsPermissions.READ_SETTINGS,
        "View detailed system setting configurations and current values",
    ),
    (
        SettingsPermissions.UPDATE_SETTINGS,
        "Modify system-wide configuration settings and parameters",
    ),
]


def list_all_permissions():
    return [
        *iam_permissions_list,
        *menu_permissions,
        *order_permissions,
        *branch_permissions,
        *settings_permissions,
    ]
