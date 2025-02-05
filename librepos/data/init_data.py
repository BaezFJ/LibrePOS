ROLES = [
    {
        "name": "admin",
        "description": "Manage all aspects, including employee roles, menus, promotions, and settings.",
    },
    {
        "name": "manager",
        "description": "Access to reports, inventory, and staff management (without system-level settings)",
    },
    {
        "name": "cashier",
        "description": "Process sales, apply discounts (if allowed), and issue receipts.  Limited access to reports (e.g., daily sales summary).",
    },
    {
        "name": "waiter / server",
        "description": "Enter orders, split bills, and send order tickets to kitchen printers or displays. Limited visibility of sales or reports.",
    },
]

PERMISSIONS = [
    # ********** Users Permissions **********
    {
        "name": "CreateUser",
        "description": "Add user username, email, roles, and permissions",
    },
    {
        "name": "GetUser",
        "description": "View user details",
    },
    {
        "name": "ListUsers",
        "description": "View users and their roles",
    },
    {
        "name": "UpdateUser",
        "description": "Edit user username, email, roles, and permissions",
    },
    {
        "name": "DeleteUser",
        "description": "Delete user from system.",
    },
]

POLICIES = [
    {
        "name": "AdministratorAccess",
        "description": "Allows full access to LibrePOS system.",
    }
]

GROUPS = [
    {"name": "Administrator", "description": "Allows full access to LibrePOS system."}
]
