from enum import StrEnum
from typing import List, Set


class Permissions(StrEnum):
    # Sales & Orders
    VIEW_ORDERS = "view_orders"
    CREATE_ORDER = "create_order"
    EDIT_ORDER = "edit_order"
    DELETE_ORDER = "delete_order"
    CANCEL_ORDER = "cancel_order"
    REFUND_ORDER = "refund_order"
    VOID_TRANSACTION = "void_transaction"

    # Payment
    PROCESS_PAYMENT = "process_payment"
    PROCESS_CASH_PAYMENT = "process_cash_payment"
    PROCESS_CARD_PAYMENT = "process_card_payment"
    PROCESS_MOBILE_PAYMENT = "process_mobile_payment"
    SPLIT_PAYMENT = "split_payment"

    # Cash Management
    OPEN_REGISTER = "open_register"
    CLOSE_REGISTER = "close_register"
    VIEW_CASH_DRAWER = "view_cash_drawer"
    MANAGE_CASH_DRAWER = "manage_cash_drawer"
    PERFORM_CASH_DROP = "perform_cash_drop"
    PERFORM_PAYOUT = "perform_payout"

    # Menu & Inventory
    VIEW_MENU = "view_menu"
    MANAGE_MENU = "manage_menu"
    VIEW_INVENTORY = "view_inventory"
    MANAGE_INVENTORY = "manage_inventory"
    ADJUST_INVENTORY = "adjust_inventory"

    # Discounts & Promotions
    APPLY_DISCOUNT = "apply_discount"
    MANAGE_DISCOUNTS = "manage_discounts"
    APPLY_COMPS = "apply_comps"

    # Tables & Reservations
    VIEW_TABLES = "view_tables"
    MANAGE_TABLES = "manage_tables"
    ASSIGN_TABLES = "assign_tables"
    VIEW_RESERVATIONS = "view_reservations"
    MANAGE_RESERVATIONS = "manage_reservations"

    # Reports
    VIEW_SALES_REPORTS = "view_sales_reports"
    VIEW_INVENTORY_REPORTS = "view_inventory_reports"
    VIEW_EMPLOYEE_REPORTS = "view_employee_reports"
    VIEW_FINANCIAL_REPORTS = "view_financial_reports"
    EXPORT_REPORTS = "export_reports"

    # Staff Management
    VIEW_EMPLOYEES = "view_employees"
    MANAGE_EMPLOYEES = "manage_employees"
    VIEW_TIMECLOCK = "view_timeclock"
    MANAGE_TIMECLOCK = "manage_timeclock"
    CLOCK_IN_OUT = "clock_in_out"

    # Customer Management
    VIEW_CUSTOMERS = "view_customers"
    MANAGE_CUSTOMERS = "manage_customers"
    VIEW_CUSTOMER_HISTORY = "view_customer_history"
    MANAGE_LOYALTY_POINTS = "manage_loyalty_points"

    # System Settings
    VIEW_SETTINGS = "view_settings"
    MANAGE_SETTINGS = "manage_settings"
    MANAGE_USERS = "manage_users"
    MANAGE_ROLES = "manage_roles"
    MANAGE_PERMISSIONS = "manage_permissions"
    VIEW_AUDIT_LOGS = "view_audit_logs"

    # Kitchen Display System
    VIEW_KITCHEN_ORDERS = "view_kitchen_orders"
    MANAGE_KITCHEN_ORDERS = "manage_kitchen_orders"
    MARK_ORDER_READY = "mark_order_ready"

    # Delivery & Takeout
    MANAGE_DELIVERY = "manage_delivery"
    ASSIGN_DELIVERY = "assign_delivery"
    MANAGE_TAKEOUT = "manage_takeout"

    # Tax Management
    VIEW_TAX_SETTINGS = "view_tax_settings"
    MANAGE_TAX_SETTINGS = "manage_tax_settings"


class Roles(StrEnum):
    OWNER = "owner"
    ADMIN = "admin"
    MANAGER = "manager"
    CASHIER = "cashier"
    WAITER = "waiter"
    BARTENDER = "bartender"
    KITCHEN_STAFF = "kitchen_staff"
    HOST = "host"
    DELIVERY_DRIVER = "delivery_driver"
    CUSTOMER = "customer"


# ============================================================================
# Permission Groups - Organized by functional area
# ============================================================================

# Common permissions all staff have
BASIC_STAFF_PERMISSIONS: List[Permissions] = [
    Permissions.CLOCK_IN_OUT,
    Permissions.VIEW_MENU,
]

# Order viewing and creation
ORDER_PERMISSIONS: List[Permissions] = [
    Permissions.VIEW_ORDERS,
    Permissions.CREATE_ORDER,
    Permissions.EDIT_ORDER,
]

# Advanced order operations (refunds, cancellations, etc.)
ADVANCED_ORDER_PERMISSIONS: List[Permissions] = [
    Permissions.DELETE_ORDER,
    Permissions.CANCEL_ORDER,
    Permissions.REFUND_ORDER,
    Permissions.VOID_TRANSACTION,
]

# All payment processing
PAYMENT_PERMISSIONS: List[Permissions] = [
    Permissions.PROCESS_PAYMENT,
    Permissions.PROCESS_CASH_PAYMENT,
    Permissions.PROCESS_CARD_PAYMENT,
    Permissions.PROCESS_MOBILE_PAYMENT,
    Permissions.SPLIT_PAYMENT,
]

# Basic register operations
REGISTER_PERMISSIONS: List[Permissions] = [
    Permissions.OPEN_REGISTER,
    Permissions.CLOSE_REGISTER,
    Permissions.VIEW_CASH_DRAWER,
    Permissions.PERFORM_CASH_DROP,
]

# Advanced cash management
CASH_MANAGEMENT_PERMISSIONS: List[Permissions] = [
    Permissions.MANAGE_CASH_DRAWER,
    Permissions.PERFORM_PAYOUT,
]

# Discount operations
DISCOUNT_PERMISSIONS: List[Permissions] = [
    Permissions.APPLY_DISCOUNT,
]

# Advanced discount management
DISCOUNT_MANAGEMENT_PERMISSIONS: List[Permissions] = [
    Permissions.MANAGE_DISCOUNTS,
    Permissions.APPLY_COMPS,
]

# Inventory viewing
INVENTORY_VIEW_PERMISSIONS: List[Permissions] = [
    Permissions.VIEW_INVENTORY,
]

# Full inventory management
INVENTORY_MANAGEMENT_PERMISSIONS: List[Permissions] = [
    Permissions.MANAGE_INVENTORY,
    Permissions.ADJUST_INVENTORY,
]

# Menu management
MENU_MANAGEMENT_PERMISSIONS: List[Permissions] = [
    Permissions.MANAGE_MENU,
]

# Table and reservation viewing/management
TABLE_PERMISSIONS: List[Permissions] = [
    Permissions.VIEW_TABLES,
    Permissions.ASSIGN_TABLES,
    Permissions.VIEW_RESERVATIONS,
]

TABLE_MANAGEMENT_PERMISSIONS: List[Permissions] = [
    Permissions.MANAGE_TABLES,
    Permissions.MANAGE_RESERVATIONS,
]

# Customer viewing
CUSTOMER_VIEW_PERMISSIONS: List[Permissions] = [
    Permissions.VIEW_CUSTOMERS,
    Permissions.VIEW_CUSTOMER_HISTORY,
]

# Customer management
CUSTOMER_MANAGEMENT_PERMISSIONS: List[Permissions] = [
    Permissions.MANAGE_CUSTOMERS,
    Permissions.MANAGE_LOYALTY_POINTS,
]

# Kitchen display system
KITCHEN_PERMISSIONS: List[Permissions] = [
    Permissions.VIEW_KITCHEN_ORDERS,
    Permissions.MANAGE_KITCHEN_ORDERS,
    Permissions.MARK_ORDER_READY,
]

# Delivery and takeout
DELIVERY_PERMISSIONS: List[Permissions] = [
    Permissions.MANAGE_DELIVERY,
    Permissions.ASSIGN_DELIVERY,
]

TAKEOUT_PERMISSIONS: List[Permissions] = [
    Permissions.MANAGE_TAKEOUT,
]

# Reporting permissions
BASIC_REPORTS_PERMISSIONS: List[Permissions] = [
    Permissions.VIEW_SALES_REPORTS,
    Permissions.VIEW_INVENTORY_REPORTS,
    Permissions.VIEW_EMPLOYEE_REPORTS,
    Permissions.EXPORT_REPORTS,
]

FINANCIAL_REPORTS_PERMISSIONS: List[Permissions] = [
    Permissions.VIEW_FINANCIAL_REPORTS,
]

# Staff management
STAFF_VIEW_PERMISSIONS: List[Permissions] = [
    Permissions.VIEW_EMPLOYEES,
    Permissions.VIEW_TIMECLOCK,
]

STAFF_MANAGEMENT_PERMISSIONS: List[Permissions] = [
    Permissions.MANAGE_EMPLOYEES,
    Permissions.MANAGE_TIMECLOCK,
]

# Settings
SETTINGS_VIEW_PERMISSIONS: List[Permissions] = [
    Permissions.VIEW_SETTINGS,
]

SETTINGS_MANAGEMENT_PERMISSIONS: List[Permissions] = [
    Permissions.MANAGE_SETTINGS,
]

# Tax management
TAX_PERMISSIONS: List[Permissions] = [
    Permissions.VIEW_TAX_SETTINGS,
    Permissions.MANAGE_TAX_SETTINGS,
]

# System administration (most sensitive)
SYSTEM_ADMIN_PERMISSIONS: List[Permissions] = [
    Permissions.MANAGE_USERS,
    Permissions.MANAGE_ROLES,
    Permissions.MANAGE_PERMISSIONS,
    Permissions.VIEW_AUDIT_LOGS,
]


# ============================================================================
# Helper Functions
# ============================================================================


def combine_permissions(*permission_groups: List[Permissions]) -> List[Permissions]:
    """Combine multiple permission groups into a single list, removing duplicates."""
    combined: Set[Permissions] = set()
    for group in permission_groups:
        combined.update(group)
    return list(combined)


def get_all_permissions() -> List[Permissions]:
    """Get all available permissions from the Permissions enum."""
    return list(Permissions)


def remove_permissions(
    base_permissions: List[Permissions], permissions_to_remove: List[Permissions]
) -> List[Permissions]:
    """Remove specific permissions from a base set."""
    return [p for p in base_permissions if p not in permissions_to_remove]


# ============================================================================
# Role Permissions - Composed from permission groups
# ============================================================================

ROLE_PERMISSIONS = {
    # Owner has ALL permissions
    Roles.OWNER: get_all_permissions(),
    # Admin has all permissions except system-critical role/permission management
    Roles.ADMIN: remove_permissions(
        get_all_permissions(),
        [Permissions.MANAGE_USERS, Permissions.MANAGE_ROLES, Permissions.MANAGE_PERMISSIONS],
    ),
    # Manager has extensive operational permissions but limited system access
    Roles.MANAGER: combine_permissions(
        BASIC_STAFF_PERMISSIONS,
        ORDER_PERMISSIONS,
        [
            Permissions.CANCEL_ORDER,
            Permissions.REFUND_ORDER,
            Permissions.VOID_TRANSACTION,
        ],  # Subset of advanced order permissions
        PAYMENT_PERMISSIONS,
        REGISTER_PERMISSIONS,
        CASH_MANAGEMENT_PERMISSIONS,
        DISCOUNT_PERMISSIONS,
        DISCOUNT_MANAGEMENT_PERMISSIONS,
        INVENTORY_VIEW_PERMISSIONS,
        [Permissions.ADJUST_INVENTORY],  # Can adjust but not fully manage inventory
        MENU_MANAGEMENT_PERMISSIONS,
        TABLE_PERMISSIONS,
        TABLE_MANAGEMENT_PERMISSIONS,
        CUSTOMER_VIEW_PERMISSIONS,
        CUSTOMER_MANAGEMENT_PERMISSIONS,
        KITCHEN_PERMISSIONS,
        DELIVERY_PERMISSIONS,
        TAKEOUT_PERMISSIONS,
        BASIC_REPORTS_PERMISSIONS,
        STAFF_VIEW_PERMISSIONS,
        [Permissions.MANAGE_TIMECLOCK],  # Can manage timeclock but not employees
        SETTINGS_VIEW_PERMISSIONS,
        [Permissions.VIEW_TAX_SETTINGS],  # Can view but not manage tax settings
    ),
    # Cashier focuses on orders, payments, and register operations
    Roles.CASHIER: combine_permissions(
        BASIC_STAFF_PERMISSIONS,
        ORDER_PERMISSIONS,
        PAYMENT_PERMISSIONS,
        REGISTER_PERMISSIONS,
        DISCOUNT_PERMISSIONS,
        CUSTOMER_VIEW_PERMISSIONS,
        TAKEOUT_PERMISSIONS,
    ),
    # Waiter handles orders, payments, and table management
    Roles.WAITER: combine_permissions(
        BASIC_STAFF_PERMISSIONS,
        ORDER_PERMISSIONS,
        PAYMENT_PERMISSIONS,
        DISCOUNT_PERMISSIONS,
        TABLE_PERMISSIONS,
        CUSTOMER_VIEW_PERMISSIONS,
    ),
    # Bartender similar to waiter but with kitchen display access
    Roles.BARTENDER: combine_permissions(
        BASIC_STAFF_PERMISSIONS,
        ORDER_PERMISSIONS,
        PAYMENT_PERMISSIONS,
        DISCOUNT_PERMISSIONS,
        [Permissions.VIEW_CUSTOMERS],  # Only view customers, not history
        [Permissions.VIEW_KITCHEN_ORDERS, Permissions.MARK_ORDER_READY],
    ),
    # Kitchen staff focuses on kitchen operations
    Roles.KITCHEN_STAFF: combine_permissions(
        BASIC_STAFF_PERMISSIONS,
        KITCHEN_PERMISSIONS,
        INVENTORY_VIEW_PERMISSIONS,
    ),
    # Host manages tables and reservations
    Roles.HOST: combine_permissions(
        [Permissions.CLOCK_IN_OUT],  # Basic staff without VIEW_MENU
        [Permissions.VIEW_ORDERS],
        TABLE_PERMISSIONS,
        TABLE_MANAGEMENT_PERMISSIONS,
        [Permissions.VIEW_CUSTOMERS],
    ),
    # Delivery driver handles deliveries and cash collection
    Roles.DELIVERY_DRIVER: combine_permissions(
        [Permissions.CLOCK_IN_OUT],  # Basic staff without VIEW_MENU
        [Permissions.VIEW_ORDERS],
        [Permissions.MANAGE_DELIVERY],  # Only manage, not assign
        [Permissions.VIEW_CUSTOMERS, Permissions.PROCESS_CASH_PAYMENT],
    ),
    # Customer has minimal view-only permissions
    Roles.CUSTOMER: [
        Permissions.VIEW_ORDERS,
        Permissions.VIEW_MENU,
        Permissions.VIEW_CUSTOMER_HISTORY,
    ],
}
