"""Main blueprint permissions and policy mappings.

This includes all POS operations: sales, orders, payments, inventory, etc.
"""

from enum import StrEnum

from librepos.permissions import PolicyDefinition


class OrderPermissions(StrEnum):
    """Permissions for order management."""

    VIEW_ORDERS = "view_orders"
    CREATE_ORDER = "create_order"
    EDIT_ORDER = "edit_order"
    DELETE_ORDER = "delete_order"
    CANCEL_ORDER = "cancel_order"
    REFUND_ORDER = "refund_order"
    VOID_TRANSACTION = "void_transaction"


class PaymentPermissions(StrEnum):
    """Permissions for payment processing."""

    PROCESS_PAYMENT = "process_payment"
    PROCESS_CASH_PAYMENT = "process_cash_payment"
    PROCESS_CARD_PAYMENT = "process_card_payment"
    PROCESS_MOBILE_PAYMENT = "process_mobile_payment"
    SPLIT_PAYMENT = "split_payment"


class CashManagementPermissions(StrEnum):
    """Permissions for cash register and drawer management."""

    OPEN_REGISTER = "open_register"
    CLOSE_REGISTER = "close_register"
    VIEW_CASH_DRAWER = "view_cash_drawer"
    MANAGE_CASH_DRAWER = "manage_cash_drawer"
    PERFORM_CASH_DROP = "perform_cash_drop"
    PERFORM_PAYOUT = "perform_payout"


class InventoryPermissions(StrEnum):
    """Permissions for inventory management."""

    VIEW_INVENTORY = "view_inventory"
    MANAGE_INVENTORY = "manage_inventory"
    ADJUST_INVENTORY = "adjust_inventory"


class MenuPermissions(StrEnum):
    """Permissions for menu management."""

    VIEW_MENU = "view_menu"
    MANAGE_MENU = "manage_menu"


class DiscountPermissions(StrEnum):
    """Permissions for discounts and promotions."""

    APPLY_DISCOUNT = "apply_discount"
    MANAGE_DISCOUNTS = "manage_discounts"
    APPLY_COMPS = "apply_comps"


class TablePermissions(StrEnum):
    """Permissions for table and reservation management."""

    VIEW_TABLES = "view_tables"
    MANAGE_TABLES = "manage_tables"
    ASSIGN_TABLES = "assign_tables"
    VIEW_RESERVATIONS = "view_reservations"
    MANAGE_RESERVATIONS = "manage_reservations"


class CustomerPermissions(StrEnum):
    """Permissions for customer management."""

    VIEW_CUSTOMERS = "view_customers"
    MANAGE_CUSTOMERS = "manage_customers"
    VIEW_CUSTOMER_HISTORY = "view_customer_history"
    MANAGE_LOYALTY_POINTS = "manage_loyalty_points"


class KitchenPermissions(StrEnum):
    """Permissions for kitchen display system."""

    VIEW_KITCHEN_ORDERS = "view_kitchen_orders"
    MANAGE_KITCHEN_ORDERS = "manage_kitchen_orders"
    MARK_ORDER_READY = "mark_order_ready"


class DeliveryPermissions(StrEnum):
    """Permissions for delivery and takeout."""

    MANAGE_DELIVERY = "manage_delivery"
    ASSIGN_DELIVERY = "assign_delivery"
    MANAGE_TAKEOUT = "manage_takeout"


class ReportPermissions(StrEnum):
    """Permissions for viewing reports."""

    VIEW_SALES_REPORTS = "view_sales_reports"
    VIEW_INVENTORY_REPORTS = "view_inventory_reports"
    VIEW_FINANCIAL_REPORTS = "view_financial_reports"
    EXPORT_REPORTS = "export_reports"


class SettingsPermissions(StrEnum):
    """Permissions for system settings."""

    VIEW_SETTINGS = "view_settings"
    MANAGE_SETTINGS = "manage_settings"


class TaxPermissions(StrEnum):
    """Permissions for tax management."""

    VIEW_TAX_SETTINGS = "view_tax_settings"
    MANAGE_TAX_SETTINGS = "manage_tax_settings"


# ============================================================================
# Default Policy Definitions
# ============================================================================

POS_FULL_ACCESS_POLICY = PolicyDefinition(
    name="POS Full Access",
    description="Complete access to all POS operations including orders, payments, inventory, and system settings",
    permissions=[
        # Orders
        OrderPermissions.VIEW_ORDERS,
        OrderPermissions.CREATE_ORDER,
        OrderPermissions.EDIT_ORDER,
        OrderPermissions.DELETE_ORDER,
        OrderPermissions.CANCEL_ORDER,
        OrderPermissions.REFUND_ORDER,
        OrderPermissions.VOID_TRANSACTION,
        # Payments
        PaymentPermissions.PROCESS_PAYMENT,
        PaymentPermissions.PROCESS_CASH_PAYMENT,
        PaymentPermissions.PROCESS_CARD_PAYMENT,
        PaymentPermissions.PROCESS_MOBILE_PAYMENT,
        PaymentPermissions.SPLIT_PAYMENT,
        # Cash Management
        CashManagementPermissions.OPEN_REGISTER,
        CashManagementPermissions.CLOSE_REGISTER,
        CashManagementPermissions.VIEW_CASH_DRAWER,
        CashManagementPermissions.MANAGE_CASH_DRAWER,
        CashManagementPermissions.PERFORM_CASH_DROP,
        CashManagementPermissions.PERFORM_PAYOUT,
        # Inventory
        InventoryPermissions.VIEW_INVENTORY,
        InventoryPermissions.MANAGE_INVENTORY,
        InventoryPermissions.ADJUST_INVENTORY,
        # Menu
        MenuPermissions.VIEW_MENU,
        MenuPermissions.MANAGE_MENU,
        # Discounts
        DiscountPermissions.APPLY_DISCOUNT,
        DiscountPermissions.MANAGE_DISCOUNTS,
        DiscountPermissions.APPLY_COMPS,
        # Tables
        TablePermissions.VIEW_TABLES,
        TablePermissions.MANAGE_TABLES,
        TablePermissions.ASSIGN_TABLES,
        TablePermissions.VIEW_RESERVATIONS,
        TablePermissions.MANAGE_RESERVATIONS,
        # Customers
        CustomerPermissions.VIEW_CUSTOMERS,
        CustomerPermissions.MANAGE_CUSTOMERS,
        CustomerPermissions.VIEW_CUSTOMER_HISTORY,
        CustomerPermissions.MANAGE_LOYALTY_POINTS,
        # Kitchen
        KitchenPermissions.VIEW_KITCHEN_ORDERS,
        KitchenPermissions.MANAGE_KITCHEN_ORDERS,
        KitchenPermissions.MARK_ORDER_READY,
        # Delivery
        DeliveryPermissions.MANAGE_DELIVERY,
        DeliveryPermissions.ASSIGN_DELIVERY,
        DeliveryPermissions.MANAGE_TAKEOUT,
        # Reports
        ReportPermissions.VIEW_SALES_REPORTS,
        ReportPermissions.VIEW_INVENTORY_REPORTS,
        ReportPermissions.VIEW_FINANCIAL_REPORTS,
        ReportPermissions.EXPORT_REPORTS,
        # Settings
        SettingsPermissions.VIEW_SETTINGS,
        SettingsPermissions.MANAGE_SETTINGS,
        # Tax
        TaxPermissions.VIEW_TAX_SETTINGS,
        TaxPermissions.MANAGE_TAX_SETTINGS,
    ],
    is_system=True,
)

POS_MANAGER_POLICY = PolicyDefinition(
    name="POS Manager Access",
    description="Manager-level access for daily operations, reports, and cash management without system configuration",
    permissions=[
        # Orders (including advanced operations)
        OrderPermissions.VIEW_ORDERS,
        OrderPermissions.CREATE_ORDER,
        OrderPermissions.EDIT_ORDER,
        OrderPermissions.CANCEL_ORDER,
        OrderPermissions.REFUND_ORDER,
        OrderPermissions.VOID_TRANSACTION,
        # Payments
        PaymentPermissions.PROCESS_PAYMENT,
        PaymentPermissions.PROCESS_CASH_PAYMENT,
        PaymentPermissions.PROCESS_CARD_PAYMENT,
        PaymentPermissions.PROCESS_MOBILE_PAYMENT,
        PaymentPermissions.SPLIT_PAYMENT,
        # Cash Management
        CashManagementPermissions.OPEN_REGISTER,
        CashManagementPermissions.CLOSE_REGISTER,
        CashManagementPermissions.VIEW_CASH_DRAWER,
        CashManagementPermissions.MANAGE_CASH_DRAWER,
        CashManagementPermissions.PERFORM_CASH_DROP,
        CashManagementPermissions.PERFORM_PAYOUT,
        InventoryPermissions.VIEW_INVENTORY,
        InventoryPermissions.ADJUST_INVENTORY,
        MenuPermissions.VIEW_MENU,
        MenuPermissions.MANAGE_MENU,
        DiscountPermissions.APPLY_DISCOUNT,
        DiscountPermissions.MANAGE_DISCOUNTS,
        DiscountPermissions.APPLY_COMPS,
        # Tables
        TablePermissions.VIEW_TABLES,
        TablePermissions.MANAGE_TABLES,
        TablePermissions.ASSIGN_TABLES,
        TablePermissions.VIEW_RESERVATIONS,
        TablePermissions.MANAGE_RESERVATIONS,
        # Customers
        CustomerPermissions.VIEW_CUSTOMERS,
        CustomerPermissions.MANAGE_CUSTOMERS,
        CustomerPermissions.VIEW_CUSTOMER_HISTORY,
        CustomerPermissions.MANAGE_LOYALTY_POINTS,
        # Kitchen
        KitchenPermissions.VIEW_KITCHEN_ORDERS,
        KitchenPermissions.MANAGE_KITCHEN_ORDERS,
        KitchenPermissions.MARK_ORDER_READY,
        # Delivery
        DeliveryPermissions.MANAGE_DELIVERY,
        DeliveryPermissions.ASSIGN_DELIVERY,
        DeliveryPermissions.MANAGE_TAKEOUT,
        # Reports
        ReportPermissions.VIEW_SALES_REPORTS,
        ReportPermissions.VIEW_INVENTORY_REPORTS,
        ReportPermissions.EXPORT_REPORTS,
        # Settings (view only)
        SettingsPermissions.VIEW_SETTINGS,
        # Tax (view only)
        TaxPermissions.VIEW_TAX_SETTINGS,
    ],
    is_system=True,
)

POS_CASHIER_POLICY = PolicyDefinition(
    name="POS Cashier Access",
    description="Cashier-level access for order processing, payments, and register operations",
    permissions=[
        MenuPermissions.VIEW_MENU,
        OrderPermissions.VIEW_ORDERS,
        OrderPermissions.CREATE_ORDER,
        OrderPermissions.EDIT_ORDER,
        PaymentPermissions.PROCESS_PAYMENT,
        PaymentPermissions.PROCESS_CASH_PAYMENT,
        PaymentPermissions.PROCESS_CARD_PAYMENT,
        PaymentPermissions.PROCESS_MOBILE_PAYMENT,
        PaymentPermissions.SPLIT_PAYMENT,
        CashManagementPermissions.OPEN_REGISTER,
        CashManagementPermissions.CLOSE_REGISTER,
        CashManagementPermissions.VIEW_CASH_DRAWER,
        CashManagementPermissions.PERFORM_CASH_DROP,
        DiscountPermissions.APPLY_DISCOUNT,
        CustomerPermissions.VIEW_CUSTOMERS,
        CustomerPermissions.VIEW_CUSTOMER_HISTORY,
        DeliveryPermissions.MANAGE_TAKEOUT,
    ],
    is_system=True,
)

POS_SERVER_POLICY = PolicyDefinition(
    name="POS Server Access",
    description="Server/waiter access for taking orders, processing payments, and managing tables",
    permissions=[
        MenuPermissions.VIEW_MENU,
        OrderPermissions.VIEW_ORDERS,
        OrderPermissions.CREATE_ORDER,
        OrderPermissions.EDIT_ORDER,
        PaymentPermissions.PROCESS_PAYMENT,
        PaymentPermissions.PROCESS_CASH_PAYMENT,
        PaymentPermissions.PROCESS_CARD_PAYMENT,
        PaymentPermissions.PROCESS_MOBILE_PAYMENT,
        PaymentPermissions.SPLIT_PAYMENT,
        DiscountPermissions.APPLY_DISCOUNT,
        TablePermissions.VIEW_TABLES,
        TablePermissions.ASSIGN_TABLES,
        TablePermissions.VIEW_RESERVATIONS,
        CustomerPermissions.VIEW_CUSTOMERS,
        CustomerPermissions.VIEW_CUSTOMER_HISTORY,
    ],
    is_system=True,
)

POS_KITCHEN_POLICY = PolicyDefinition(
    name="POS Kitchen Access",
    description="Kitchen staff access for viewing and managing kitchen orders",
    permissions=[
        MenuPermissions.VIEW_MENU,
        KitchenPermissions.VIEW_KITCHEN_ORDERS,
        KitchenPermissions.MANAGE_KITCHEN_ORDERS,
        KitchenPermissions.MARK_ORDER_READY,
        InventoryPermissions.VIEW_INVENTORY,
    ],
    is_system=True,
)

POS_HOST_POLICY = PolicyDefinition(
    name="POS Host Access",
    description="Host/hostess access for managing tables and reservations",
    permissions=[
        OrderPermissions.VIEW_ORDERS,
        TablePermissions.VIEW_TABLES,
        TablePermissions.MANAGE_TABLES,
        TablePermissions.ASSIGN_TABLES,
        TablePermissions.VIEW_RESERVATIONS,
        TablePermissions.MANAGE_RESERVATIONS,
        CustomerPermissions.VIEW_CUSTOMERS,
    ],
    is_system=True,
)

POS_DELIVERY_POLICY = PolicyDefinition(
    name="POS Delivery Driver Access",
    description="Delivery driver access for managing deliveries and collecting payments",
    permissions=[
        OrderPermissions.VIEW_ORDERS,
        DeliveryPermissions.MANAGE_DELIVERY,
        CustomerPermissions.VIEW_CUSTOMERS,
        PaymentPermissions.PROCESS_CASH_PAYMENT,
    ],
    is_system=True,
)

POS_READ_ONLY_POLICY = PolicyDefinition(
    name="POS Read Only",
    description="View-only access to POS data for reporting and analysis",
    permissions=[
        MenuPermissions.VIEW_MENU,
        OrderPermissions.VIEW_ORDERS,
        InventoryPermissions.VIEW_INVENTORY,
        TablePermissions.VIEW_TABLES,
        TablePermissions.VIEW_RESERVATIONS,
        CustomerPermissions.VIEW_CUSTOMERS,
        CustomerPermissions.VIEW_CUSTOMER_HISTORY,
        ReportPermissions.VIEW_SALES_REPORTS,
        ReportPermissions.VIEW_INVENTORY_REPORTS,
        SettingsPermissions.VIEW_SETTINGS,
        TaxPermissions.VIEW_TAX_SETTINGS,
    ],
    is_system=True,
)

# Collection of all default policies for this blueprint
DEFAULT_POLICIES = [
    POS_FULL_ACCESS_POLICY,
    POS_MANAGER_POLICY,
    POS_CASHIER_POLICY,
    POS_SERVER_POLICY,
    POS_KITCHEN_POLICY,
    POS_HOST_POLICY,
    POS_DELIVERY_POLICY,
    POS_READ_ONLY_POLICY,
]
