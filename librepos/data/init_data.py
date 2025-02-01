ROLES = [
    {
        "name": "admin",
        "description": "Manage all aspects, including employee roles, menus, promotions, and settings.",
        "is_removable": False,
        "is_admin": True,
    },
    {
        "name": "manager",
        "description": "Access to reports, inventory, and staff management (without system-level settings)",
        "is_removable": False,
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
        "name": "create_user",
        "description": "Add user username, email, roles, and permissions",
    },
    {
        "name": "get_user",
        "description": "View user details",
    },
    {
        "name": "list_users",
        "description": "View users and their roles",
    },
    {
        "name": "update_user",
        "description": "Edit user username, email, roles, and permissions",
    },
    {
        "name": "delete_user",
        "description": "Delete user from system.",
    },
    # ********** Business Permissions **********
    {"name": "update_business", "description": "Edit business details"},
    {"name": "get_business", "description": "View business details"},
    # ********** Device Permissions **********
    {
        "name": "update_device",
        "description": "Edit device details",
    },
    {"name": "get_device", "description": "View device details"},
    {"name": "list_devices", "description": "View devices"},
    {"name": "create_device", "description": "Add new device"},
    {"name": "delete_device", "description": "Delete device"},
    # ********** Table Permissions **********
    {"name": "create_table", "description": "Add new table"},
    {"name": "get_table", "description": "View table details"},
    {"name": "list_tables", "description": "View tables"},
    {"name": "update_table", "description": "Edit table"},
    {"name": "delete_table", "description": "Delete table"},
]
