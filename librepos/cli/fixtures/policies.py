from librepos.features.branches.utils.enums import BranchPermissions
from librepos.features.iam.utils.enums import IAMPermissions
from librepos.features.menu.utils.enums import MenuPermissions
from librepos.features.orders.utils.enums import OrderPermissions
from librepos.features.settings.utils.enums import SettingsPermissions
from .permission_utils import PermissionLevelManager

IAM_POLICIES = [
    (
        "IAMFullAccess",
        "Provides complete access to all IAM features including user, role, and policy management with full create, read, update, and delete capabilities",
        PermissionLevelManager.get_full_access_permissions(IAMPermissions),
    ),
    (
        "IAMLimitedAccess",
        "Provides access to view and modify IAM resources but restricts creation and deletion of users, roles, and policies",
        PermissionLevelManager.get_limited_access_permissions(IAMPermissions),
    ),
    (
        "IAMReadOnlyAccess",
        "Provides view-only access to IAM resources including users, roles, and policies without modification capabilities",
        PermissionLevelManager.get_read_only_permissions(IAMPermissions),
    ),
    (
        "IAMUserFull",
        "Provides complete user management capabilities including creating, viewing, updating, and deleting user accounts",
        [
            IAMPermissions.ACCESS,
            IAMPermissions.CREATE_USER,
            IAMPermissions.READ_USER,
            IAMPermissions.LIST_USER,
            IAMPermissions.UPDATE_USER,
            IAMPermissions.DELETE_USER,
        ],
    ),
    (
        "IAMUserLimited",
        "Provides ability to view and modify user accounts but restricts user creation and deletion",
        [
            IAMPermissions.ACCESS,
            IAMPermissions.READ_USER,
            IAMPermissions.LIST_USER,
            IAMPermissions.UPDATE_USER,
        ],
    ),
    (
        "IAMUserReadOnly",
        "Provides view-only access to user account information without modification capabilities",
        [IAMPermissions.ACCESS, IAMPermissions.READ_USER, IAMPermissions.LIST_USER],
    ),
    (
        "IAMRoleFull",
        "Provides complete role management capabilities including creating, viewing, updating, and deleting roles",
        [
            IAMPermissions.ACCESS,
            IAMPermissions.CREATE_ROLE,
            IAMPermissions.READ_ROLE,
            IAMPermissions.LIST_ROLE,
            IAMPermissions.UPDATE_ROLE,
            IAMPermissions.DELETE_ROLE,
        ],
    ),
    (
        "IAMRoleLimited",
        "Provides ability to view and modify roles but restricts role creation and deletion",
        [
            IAMPermissions.ACCESS,
            IAMPermissions.READ_ROLE,
            IAMPermissions.LIST_ROLE,
            IAMPermissions.UPDATE_ROLE,
        ],
    ),
    (
        "IAMRoleReadOnly",
        "Provides view-only access to role configurations without modification capabilities",
        [IAMPermissions.ACCESS, IAMPermissions.READ_ROLE, IAMPermissions.LIST_ROLE],
    ),
    (
        "IAMPolicyFull",
        "Provides complete policy management capabilities including creating, viewing, updating, and deleting policies",
        [
            IAMPermissions.ACCESS,
            IAMPermissions.CREATE_POLICY,
            IAMPermissions.READ_POLICY,
            IAMPermissions.LIST_POLICY,
            IAMPermissions.UPDATE_POLICY,
            IAMPermissions.DELETE_POLICY,
        ],
    ),
    (
        "IAMPolicyLimited",
        "Provides ability to view and modify policies but restricts policy creation and deletion",
        [
            IAMPermissions.ACCESS,
            IAMPermissions.READ_POLICY,
            IAMPermissions.LIST_POLICY,
            IAMPermissions.UPDATE_POLICY,
        ],
    ),
    (
        "IAMPolicyReadOnly",
        "Provides view-only access to policy configurations without modification capabilities",
        [IAMPermissions.ACCESS, IAMPermissions.READ_POLICY, IAMPermissions.LIST_POLICY],
    ),
]

MENU_POLICIES = [
    (
        "MenuFullAccess",
        "Provides complete access to all menu management features including creation, modification and deletion of categories, groups and items",
        PermissionLevelManager.get_full_access_permissions(MenuPermissions),
    ),
    (
        "MenuLimitedAccess",
        "Provides ability to view and modify menu items, categories and groups but restricts creation and deletion operations",
        PermissionLevelManager.get_limited_access_permissions(MenuPermissions),
    ),
    (
        "MenuReadOnlyAccess",
        "Provides view-only access to browse menu structure, categories, groups and items without modification capabilities",
        PermissionLevelManager.get_read_only_permissions(MenuPermissions),
    ),
    (
        "MenuCategoryFull",
        "Provides complete menu category management including ability to create new categories, modify existing ones, and remove categories with their contents",
        [
            MenuPermissions.ACCESS,
            MenuPermissions.CREATE_CATEGORY,
            MenuPermissions.READ_CATEGORY,
            MenuPermissions.LIST_CATEGORY,
            MenuPermissions.UPDATE_CATEGORY,
            MenuPermissions.DELETE_CATEGORY,
        ],
    ),
    (
        "MenuCategoryLimited",
        "Provides ability to view and modify existing menu categories but restricts creating new categories or deleting them",
        [
            MenuPermissions.ACCESS,
            MenuPermissions.READ_CATEGORY,
            MenuPermissions.LIST_CATEGORY,
            MenuPermissions.UPDATE_CATEGORY,
        ],
    ),
    (
        "MenuCategoryReadOnly",
        "Provides view-only access to browse menu categories and their contents without modification capabilities",
        [
            MenuPermissions.ACCESS,
            MenuPermissions.READ_CATEGORY,
            MenuPermissions.LIST_CATEGORY,
        ],
    ),
    (
        "MenuGroupFull",
        "Provides complete menu group management including ability to create new groups within categories, modify existing ones, and remove groups",
        [
            MenuPermissions.ACCESS,
            MenuPermissions.CREATE_GROUP,
            MenuPermissions.READ_GROUP,
            MenuPermissions.LIST_GROUP,
            MenuPermissions.UPDATE_GROUP,
            MenuPermissions.DELETE_GROUP,
        ],
    ),
    (
        "MenuGroupLimited",
        "Provides ability to view and modify existing menu groups but restricts creating new groups or deleting them",
        [
            MenuPermissions.ACCESS,
            MenuPermissions.READ_GROUP,
            MenuPermissions.LIST_GROUP,
            MenuPermissions.UPDATE_GROUP,
        ],
    ),
    (
        "MenuGroupReadOnly",
        "Provides view-only access to browse menu groups and their organizational structure without modification capabilities",
        [
            MenuPermissions.ACCESS,
            MenuPermissions.READ_GROUP,
            MenuPermissions.LIST_GROUP,
        ],
    ),
    (
        "MenuItemFull",
        "Provides complete menu item management including ability to add new items, modify details like pricing and descriptions, and remove items",
        [
            MenuPermissions.ACCESS,
            MenuPermissions.CREATE_ITEM,
            MenuPermissions.READ_ITEM,
            MenuPermissions.LIST_ITEM,
            MenuPermissions.UPDATE_ITEM,
            MenuPermissions.DELETE_ITEM,
        ],
    ),
    (
        "MenuItemLimited",
        "Provides ability to view and modify existing menu items but restricts adding new items or deleting them",
        [
            MenuPermissions.ACCESS,
            MenuPermissions.READ_ITEM,
            MenuPermissions.LIST_ITEM,
            MenuPermissions.UPDATE_ITEM,
        ],
    ),
    (
        "MenuItemReadOnly",
        "Provides view-only access to browse menu items and their details without modification capabilities",
        [MenuPermissions.ACCESS, MenuPermissions.READ_ITEM, MenuPermissions.LIST_ITEM],
    ),
]

ORDER_POLICIES = [
    (
        "OrderFullAccess",
        "Provides complete access to all order management functions including creating, viewing, modifying and deleting orders, tickets and items",
        PermissionLevelManager.get_full_access_permissions(OrderPermissions),
    ),
    (
        "OrderLimitedAccess",
        "Provides ability to view and modify orders but restricts creation and deletion of orders, tickets and items",
        PermissionLevelManager.get_limited_access_permissions(OrderPermissions),
    ),
    (
        "OrderReadOnlyAccess",
        "Provides view-only access to browse orders, tickets and items without modification capabilities",
        PermissionLevelManager.get_read_only_permissions(OrderPermissions),
    ),
    (
        "OrderTicketFull",
        "Provides complete order ticket management capabilities including creating new tickets, modifying ticket details like status and payment info, and removing tickets",
        [
            OrderPermissions.ACCESS,
            OrderPermissions.CREATE_TICKET,
            OrderPermissions.READ_TICKET,
            OrderPermissions.LIST_TICKET,
            OrderPermissions.UPDATE_TICKET,
            OrderPermissions.DELETE_TICKET,
        ],
    ),
    (
        "OrderTicketLimited",
        "Provides ability to view ticket details and modify ticket status and payment info but restricts creating new tickets or deleting existing ones",
        [
            OrderPermissions.ACCESS,
            OrderPermissions.READ_TICKET,
            OrderPermissions.LIST_TICKET,
            OrderPermissions.UPDATE_TICKET,
        ],
    ),
    (
        "OrderTicketReadOnly",
        "Provides view-only access to browse order tickets and their details without modification capabilities",
        [
            OrderPermissions.ACCESS,
            OrderPermissions.READ_TICKET,
            OrderPermissions.LIST_TICKET,
        ],
    ),
    (
        "OrderTicketItemFull",
        "Provides complete order item management capabilities including adding items to tickets, modifying quantities and special instructions, and removing items",
        [
            OrderPermissions.ACCESS,
            OrderPermissions.CREATE_TICKET_ITEM,
            OrderPermissions.READ_TICKET_ITEM,
            OrderPermissions.LIST_TICKET_ITEM,
            OrderPermissions.UPDATE_TICKET_ITEM,
            OrderPermissions.DELETE_TICKET_ITEM,
        ],
    ),
    (
        "OrderTicketItemLimited",
        "Provides ability to view order items and modify quantities and instructions but restricts adding new items or removing existing ones",
        [
            OrderPermissions.ACCESS,
            OrderPermissions.READ_TICKET_ITEM,
            OrderPermissions.LIST_TICKET_ITEM,
            OrderPermissions.UPDATE_TICKET_ITEM,
        ],
    ),
    (
        "OrderTicketItemReadOnly",
        "Provides view-only access to browse order items and their details without modification capabilities",
        [
            OrderPermissions.ACCESS,
            OrderPermissions.READ_TICKET_ITEM,
            OrderPermissions.LIST_TICKET_ITEM,
        ],
    ),
]

BRANCH_POLICIES = [
    (
        "BranchFullAccess",
        "Provides complete access to branch management including creating new locations, modifying branch details, and removing branches",
        PermissionLevelManager.get_full_access_permissions(BranchPermissions),
    ),
    (
        "BranchLimitedAccess",
        "Provides ability to view and modify branch details like contact info and operational settings but restricts creating or deleting branches",
        PermissionLevelManager.get_limited_access_permissions(BranchPermissions),
    ),
    (
        "BranchReadOnlyAccess",
        "Provides view-only access to browse branch locations and their details without modification capabilities",
        PermissionLevelManager.get_read_only_permissions(BranchPermissions),
    ),
]

SETTINGS_POLICIES = [
    (
        "SettingsFullAccess",
        "Provides complete access to system settings including viewing and modifying all configuration parameters and global settings",
        PermissionLevelManager.get_full_access_permissions(SettingsPermissions),
    ),
    (
        "SettingsLimitedAccess",
        "Provides ability to view and modify basic system settings while restricting access to critical configuration parameters",
        PermissionLevelManager.get_limited_access_permissions(SettingsPermissions),
    ),
    (
        "SettingsReadOnlyAccess",
        "Provides view-only access to browse system settings and configuration values without modification capabilities",
        PermissionLevelManager.get_read_only_permissions(SettingsPermissions),
    ),
]


def list_all_policies():
    """List all policy definitions."""
    return [
        *IAM_POLICIES,
        *MENU_POLICIES,
        *ORDER_POLICIES,
        *BRANCH_POLICIES,
        *SETTINGS_POLICIES,
    ]
