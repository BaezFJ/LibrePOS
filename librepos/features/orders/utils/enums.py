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
