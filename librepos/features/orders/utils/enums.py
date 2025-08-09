from enum import StrEnum


class OrderPermissions(StrEnum):
    """Order Management Permissions Enum defining access control for orders and tickets.

    This enum defines the permissions used for Order Management functionality
    across the application.

    The permissions are organized into the following categories:
    - Base access: General order system access permission
    - Ticket: Permissions for managing order tickets
    - Ticket-Item: Permissions for managing individual items on tickets

    Each permission follows the format: order.<action>.<resource>

    Example usage:
        @permission_required(OrderPermissions.CREATE_TICKET)
        def create_order():
            # Function implementation
            pass

        # Compare permissions
        if user_permission == OrderPermissions.UPDATE_TICKET_ITEM:
            # Handle update ticket item permission
            pass
    """

    # Base access
    ACCESS = "order.allow.access"

    # Ticket
    CREATE_TICKET = "order.create.ticket"
    READ_TICKET = "order.read.ticket"
    LIST_TICKET = "order.list.ticket"
    UPDATE_TICKET = "order.update.ticket"
    DELETE_TICKET = "order.delete.ticket"

    # Ticket-Item
    CREATE_TICKET_ITEM = "order.create.ticket_item"
    READ_TICKET_ITEM = "order.read.ticket_item"
    LIST_TICKET_ITEM = "order.list.ticket_item"
    UPDATE_TICKET_ITEM = "order.update.ticket_item"
    DELETE_TICKET_ITEM = "order.delete.ticket_item"

    @property
    def description(self) -> str:
        return _DESCRIPTIONS[self]


_DESCRIPTIONS: dict[OrderPermissions, str] = {
    OrderPermissions.ACCESS: "View and navigate the Order Management interface for processing customer orders",
    OrderPermissions.CREATE_TICKET: "Create new order tickets with customer and table information",
    OrderPermissions.READ_TICKET: "View detailed order ticket information including items, status and payment details",
    OrderPermissions.LIST_TICKET: "View and search through all order tickets with their current status",
    OrderPermissions.UPDATE_TICKET: "Modify existing order ticket details including status, items and payment information",
    OrderPermissions.DELETE_TICKET: "Permanently remove order tickets from the system",
    OrderPermissions.CREATE_TICKET_ITEM: "Add individual menu items to order tickets with quantity and special instructions",
    OrderPermissions.READ_TICKET_ITEM: "View detailed order item information including modifiers and preparation status",
    OrderPermissions.LIST_TICKET_ITEM: "View all items across order tickets with their current status",
    OrderPermissions.UPDATE_TICKET_ITEM: "Modify ordered items including quantity, special instructions and preparation status",
    OrderPermissions.DELETE_TICKET_ITEM: "Remove individual items from order tickets",
}


class OrderStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    VOIDED = "voided"
