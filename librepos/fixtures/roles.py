"""Role definitions for database seeding."""

ROLES_FIXTURE = [
    [
        (
            "admin",
            "Full system access with ability to manage users, roles, permissions, and all system settings",
        ),
        (
            "manager",
            "Oversees daily operations, manages staff, handles customer relations, and access to operational reports",
        ),
        (
            "cashier",
            "Handles payment processing, manages transactions, and maintains cash register operations",
        ),
        (
            "waiter",
            "Takes customer orders, serves food and beverages, and manages table service operations",
        ),
        (
            "head_chef",
            "Manages kitchen operations, creates menus, oversees food quality, and coordinates kitchen staff",
        ),
        (
            "kitchen_manager",
            "Controls inventory, manages food costs, coordinates with suppliers, and ensures food safety compliance",
        ),
        (
            "prep_cook",
            "Prepares ingredients, assists in food preparation, and maintains kitchen cleanliness standards",
        ),
        (
            "bartender",
            "Manages bar operations, prepares beverages, maintains bar inventory, and processes bar orders",
        ),
        (
            "host",
            "Manages restaurant seating, coordinates reservations, and ensures customer satisfaction upon arrival",
        ),
        (
            "accountant",
            "Handles financial records, processes payroll, manages expenses, and generates financial reports",
        ),
        (
            "inventory_manager",
            "Tracks stock levels, manages supplies, coordinates with vendors, and prevents inventory loss",
        ),
    ]
]
