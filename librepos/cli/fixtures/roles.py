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
            "bartender",
            "Manages bar operations, prepares beverages, maintains bar inventory, and processes bar orders",
        ),
        (
            "host",
            "Manages restaurant seating, coordinates reservations, and ensures customer satisfaction upon arrival",
        ),
    ]
]
