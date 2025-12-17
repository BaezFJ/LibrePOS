from enum import StrEnum


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


ROLE_PERMISSIONS = {
    Roles.OWNER: [
        # All permissions
        Permissions.VIEW_ORDERS,
        Permissions.CREATE_ORDER,
        Permissions.EDIT_ORDER,
        Permissions.DELETE_ORDER,
        Permissions.CANCEL_ORDER,
        Permissions.REFUND_ORDER,
        Permissions.VOID_TRANSACTION,
        Permissions.PROCESS_PAYMENT,
        Permissions.PROCESS_CASH_PAYMENT,
        Permissions.PROCESS_CARD_PAYMENT,
        Permissions.PROCESS_MOBILE_PAYMENT,
        Permissions.SPLIT_PAYMENT,
        Permissions.OPEN_REGISTER,
        Permissions.CLOSE_REGISTER,
        Permissions.VIEW_CASH_DRAWER,
        Permissions.MANAGE_CASH_DRAWER,
        Permissions.PERFORM_CASH_DROP,
        Permissions.PERFORM_PAYOUT,
        Permissions.VIEW_MENU,
        Permissions.MANAGE_MENU,
        Permissions.VIEW_INVENTORY,
        Permissions.MANAGE_INVENTORY,
        Permissions.ADJUST_INVENTORY,
        Permissions.APPLY_DISCOUNT,
        Permissions.MANAGE_DISCOUNTS,
        Permissions.APPLY_COMPS,
        Permissions.VIEW_TABLES,
        Permissions.MANAGE_TABLES,
        Permissions.ASSIGN_TABLES,
        Permissions.VIEW_RESERVATIONS,
        Permissions.MANAGE_RESERVATIONS,
        Permissions.VIEW_SALES_REPORTS,
        Permissions.VIEW_INVENTORY_REPORTS,
        Permissions.VIEW_EMPLOYEE_REPORTS,
        Permissions.VIEW_FINANCIAL_REPORTS,
        Permissions.EXPORT_REPORTS,
        Permissions.VIEW_EMPLOYEES,
        Permissions.MANAGE_EMPLOYEES,
        Permissions.VIEW_TIMECLOCK,
        Permissions.MANAGE_TIMECLOCK,
        Permissions.CLOCK_IN_OUT,
        Permissions.VIEW_CUSTOMERS,
        Permissions.MANAGE_CUSTOMERS,
        Permissions.VIEW_CUSTOMER_HISTORY,
        Permissions.MANAGE_LOYALTY_POINTS,
        Permissions.VIEW_SETTINGS,
        Permissions.MANAGE_SETTINGS,
        Permissions.MANAGE_USERS,
        Permissions.MANAGE_ROLES,
        Permissions.MANAGE_PERMISSIONS,
        Permissions.VIEW_AUDIT_LOGS,
        Permissions.VIEW_KITCHEN_ORDERS,
        Permissions.MANAGE_KITCHEN_ORDERS,
        Permissions.MARK_ORDER_READY,
        Permissions.MANAGE_DELIVERY,
        Permissions.ASSIGN_DELIVERY,
        Permissions.MANAGE_TAKEOUT,
        Permissions.VIEW_TAX_SETTINGS,
        Permissions.MANAGE_TAX_SETTINGS,
    ],
    Roles.ADMIN: [
        # Most permissions except system-critical ones
        Permissions.VIEW_ORDERS,
        Permissions.CREATE_ORDER,
        Permissions.EDIT_ORDER,
        Permissions.DELETE_ORDER,
        Permissions.CANCEL_ORDER,
        Permissions.REFUND_ORDER,
        Permissions.VOID_TRANSACTION,
        Permissions.PROCESS_PAYMENT,
        Permissions.PROCESS_CASH_PAYMENT,
        Permissions.PROCESS_CARD_PAYMENT,
        Permissions.PROCESS_MOBILE_PAYMENT,
        Permissions.SPLIT_PAYMENT,
        Permissions.OPEN_REGISTER,
        Permissions.CLOSE_REGISTER,
        Permissions.VIEW_CASH_DRAWER,
        Permissions.MANAGE_CASH_DRAWER,
        Permissions.PERFORM_CASH_DROP,
        Permissions.PERFORM_PAYOUT,
        Permissions.VIEW_MENU,
        Permissions.MANAGE_MENU,
        Permissions.VIEW_INVENTORY,
        Permissions.MANAGE_INVENTORY,
        Permissions.ADJUST_INVENTORY,
        Permissions.APPLY_DISCOUNT,
        Permissions.MANAGE_DISCOUNTS,
        Permissions.APPLY_COMPS,
        Permissions.VIEW_TABLES,
        Permissions.MANAGE_TABLES,
        Permissions.ASSIGN_TABLES,
        Permissions.VIEW_RESERVATIONS,
        Permissions.MANAGE_RESERVATIONS,
        Permissions.VIEW_SALES_REPORTS,
        Permissions.VIEW_INVENTORY_REPORTS,
        Permissions.VIEW_EMPLOYEE_REPORTS,
        Permissions.VIEW_FINANCIAL_REPORTS,
        Permissions.EXPORT_REPORTS,
        Permissions.VIEW_EMPLOYEES,
        Permissions.MANAGE_EMPLOYEES,
        Permissions.VIEW_TIMECLOCK,
        Permissions.MANAGE_TIMECLOCK,
        Permissions.CLOCK_IN_OUT,
        Permissions.VIEW_CUSTOMERS,
        Permissions.MANAGE_CUSTOMERS,
        Permissions.VIEW_CUSTOMER_HISTORY,
        Permissions.MANAGE_LOYALTY_POINTS,
        Permissions.VIEW_SETTINGS,
        Permissions.MANAGE_SETTINGS,
        Permissions.VIEW_AUDIT_LOGS,
        Permissions.VIEW_KITCHEN_ORDERS,
        Permissions.MANAGE_KITCHEN_ORDERS,
        Permissions.MARK_ORDER_READY,
        Permissions.MANAGE_DELIVERY,
        Permissions.ASSIGN_DELIVERY,
        Permissions.MANAGE_TAKEOUT,
        Permissions.VIEW_TAX_SETTINGS,
        Permissions.MANAGE_TAX_SETTINGS,
    ],
    Roles.MANAGER: [
        # Manager-level permissions
        Permissions.VIEW_ORDERS,
        Permissions.CREATE_ORDER,
        Permissions.EDIT_ORDER,
        Permissions.CANCEL_ORDER,
        Permissions.REFUND_ORDER,
        Permissions.VOID_TRANSACTION,
        Permissions.PROCESS_PAYMENT,
        Permissions.PROCESS_CASH_PAYMENT,
        Permissions.PROCESS_CARD_PAYMENT,
        Permissions.PROCESS_MOBILE_PAYMENT,
        Permissions.SPLIT_PAYMENT,
        Permissions.OPEN_REGISTER,
        Permissions.CLOSE_REGISTER,
        Permissions.VIEW_CASH_DRAWER,
        Permissions.MANAGE_CASH_DRAWER,
        Permissions.PERFORM_CASH_DROP,
        Permissions.PERFORM_PAYOUT,
        Permissions.VIEW_MENU,
        Permissions.MANAGE_MENU,
        Permissions.VIEW_INVENTORY,
        Permissions.ADJUST_INVENTORY,
        Permissions.APPLY_DISCOUNT,
        Permissions.MANAGE_DISCOUNTS,
        Permissions.APPLY_COMPS,
        Permissions.VIEW_TABLES,
        Permissions.MANAGE_TABLES,
        Permissions.ASSIGN_TABLES,
        Permissions.VIEW_RESERVATIONS,
        Permissions.MANAGE_RESERVATIONS,
        Permissions.VIEW_SALES_REPORTS,
        Permissions.VIEW_INVENTORY_REPORTS,
        Permissions.VIEW_EMPLOYEE_REPORTS,
        Permissions.EXPORT_REPORTS,
        Permissions.VIEW_EMPLOYEES,
        Permissions.VIEW_TIMECLOCK,
        Permissions.MANAGE_TIMECLOCK,
        Permissions.CLOCK_IN_OUT,
        Permissions.VIEW_CUSTOMERS,
        Permissions.MANAGE_CUSTOMERS,
        Permissions.VIEW_CUSTOMER_HISTORY,
        Permissions.MANAGE_LOYALTY_POINTS,
        Permissions.VIEW_SETTINGS,
        Permissions.VIEW_KITCHEN_ORDERS,
        Permissions.MANAGE_KITCHEN_ORDERS,
        Permissions.MARK_ORDER_READY,
        Permissions.MANAGE_DELIVERY,
        Permissions.ASSIGN_DELIVERY,
        Permissions.MANAGE_TAKEOUT,
        Permissions.VIEW_TAX_SETTINGS,
    ],
    Roles.CASHIER: [
        # Cashier-specific permissions
        Permissions.VIEW_ORDERS,
        Permissions.CREATE_ORDER,
        Permissions.EDIT_ORDER,
        Permissions.PROCESS_PAYMENT,
        Permissions.PROCESS_CASH_PAYMENT,
        Permissions.PROCESS_CARD_PAYMENT,
        Permissions.PROCESS_MOBILE_PAYMENT,
        Permissions.SPLIT_PAYMENT,
        Permissions.OPEN_REGISTER,
        Permissions.CLOSE_REGISTER,
        Permissions.VIEW_CASH_DRAWER,
        Permissions.PERFORM_CASH_DROP,
        Permissions.VIEW_MENU,
        Permissions.APPLY_DISCOUNT,
        Permissions.VIEW_CUSTOMERS,
        Permissions.VIEW_CUSTOMER_HISTORY,
        Permissions.CLOCK_IN_OUT,
        Permissions.MANAGE_TAKEOUT,
    ],
    Roles.WAITER: [
        # Waiter-specific permissions
        Permissions.VIEW_ORDERS,
        Permissions.CREATE_ORDER,
        Permissions.EDIT_ORDER,
        Permissions.VIEW_MENU,
        Permissions.APPLY_DISCOUNT,
        Permissions.VIEW_TABLES,
        Permissions.ASSIGN_TABLES,
        Permissions.VIEW_RESERVATIONS,
        Permissions.VIEW_CUSTOMERS,
        Permissions.VIEW_CUSTOMER_HISTORY,
        Permissions.CLOCK_IN_OUT,
        Permissions.PROCESS_PAYMENT,
        Permissions.PROCESS_CASH_PAYMENT,
        Permissions.PROCESS_CARD_PAYMENT,
        Permissions.PROCESS_MOBILE_PAYMENT,
        Permissions.SPLIT_PAYMENT,
    ],
    Roles.BARTENDER: [
        # Bartender-specific permissions
        Permissions.VIEW_ORDERS,
        Permissions.CREATE_ORDER,
        Permissions.EDIT_ORDER,
        Permissions.VIEW_MENU,
        Permissions.APPLY_DISCOUNT,
        Permissions.VIEW_KITCHEN_ORDERS,
        Permissions.MARK_ORDER_READY,
        Permissions.CLOCK_IN_OUT,
        Permissions.PROCESS_PAYMENT,
        Permissions.PROCESS_CASH_PAYMENT,
        Permissions.PROCESS_CARD_PAYMENT,
        Permissions.PROCESS_MOBILE_PAYMENT,
        Permissions.SPLIT_PAYMENT,
        Permissions.VIEW_CUSTOMERS,
    ],
    Roles.KITCHEN_STAFF: [
        # Kitchen staff permissions
        Permissions.VIEW_KITCHEN_ORDERS,
        Permissions.MANAGE_KITCHEN_ORDERS,
        Permissions.MARK_ORDER_READY,
        Permissions.VIEW_MENU,
        Permissions.VIEW_INVENTORY,
        Permissions.CLOCK_IN_OUT,
    ],
    Roles.HOST: [
        # Host-specific permissions
        Permissions.VIEW_ORDERS,
        Permissions.VIEW_TABLES,
        Permissions.MANAGE_TABLES,
        Permissions.ASSIGN_TABLES,
        Permissions.VIEW_RESERVATIONS,
        Permissions.MANAGE_RESERVATIONS,
        Permissions.VIEW_CUSTOMERS,
        Permissions.CLOCK_IN_OUT,
    ],
    Roles.DELIVERY_DRIVER: [
        # Delivery driver permissions
        Permissions.VIEW_ORDERS,
        Permissions.MANAGE_DELIVERY,
        Permissions.VIEW_CUSTOMERS,
        Permissions.CLOCK_IN_OUT,
        Permissions.PROCESS_CASH_PAYMENT,
    ],
    Roles.CUSTOMER: [
        # Customer permissions
        Permissions.VIEW_ORDERS,
        Permissions.VIEW_MENU,
        Permissions.VIEW_CUSTOMER_HISTORY,
    ],
}
