"""Policies definitions for database seeding."""

POLICIES_FIXTURE = [
    [
        ("administrator", "Allows full access to LibrePOS system."),
        (
            "manager",
            "Limited access to reports, inventory, and staff management (without system-level settings)",
        ),
        ("cashier", "Limited access to reports (e.g., daily sales summary)."),
        ("waiter", "Limited visibility of sales or reports."),
    ]
]
