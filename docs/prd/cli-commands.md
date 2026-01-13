# CLI Commands

> Application, testing, database, utility, and report commands

---

## Application Commands (`flask pos`)

| Command | Description |
|---------|-------------|
| `flask pos init-db` | Create all database tables |
| `flask pos seed` | Seed database with sample development data |
| `flask pos seed --production` | Seed required data only (roles, permissions, tax rates) |
| `flask pos create-admin` | Interactive admin user creation wizard |
| `flask pos reset-db` | Drop all tables, recreate, and seed (development only) |

---

## Testing Commands (`flask test`)

| Command | Description |
|---------|-------------|
| `flask test` | Run complete test suite |
| `flask test --coverage` | Run tests with coverage report generation |
| `flask test --blueprint menu` | Run tests for a specific blueprint only |
| `flask test --unit` | Run unit tests only |
| `flask test --integration` | Run integration tests only |

---

## Database Commands (`flask db`)

| Command | Description |
|---------|-------------|
| `flask db migrate -m "msg"` | Generate new migration with message |
| `flask db upgrade` | Apply pending migrations |
| `flask db downgrade` | Rollback last migration |
| `flask db current` | Show current migration revision |
| `flask db history` | Show migration history |

---

## Utility Commands (`flask util`)

| Command | Description |
|---------|-------------|
| `flask util routes` | List all registered routes with methods |
| `flask util permissions` | List all defined permissions by category |
| `flask util clear-sessions` | Clear expired sessions from database |
| `flask util export-schema` | Export OpenAPI schema for API documentation |

---

## Report Commands (`flask report`)

| Command | Description |
|---------|-------------|
| `flask report daily --date YYYY-MM-DD` | Generate daily summary for specified date |
| `flask report eod` | Run end-of-day process and generate reports |

---

## Seed Data Requirements

### System Roles

| Role | Description |
|------|-------------|
| Admin | Full system access |
| Manager | Operational control and reporting |
| Server | Order entry and table management |
| Bartender | Bar orders and tab management |
| Cashier | Payment processing |
| Host | Reservations and seating |
| Kitchen | Kitchen display access |
| Expo | Expeditor view and coordination |

### Permissions by Category

**Orders:** `create_order`, `modify_order`, `void_item`, `void_order`, `comp_item`, `transfer_check`

**Payments:** `process_payment`, `apply_discount`, `process_refund`, `open_drawer`, `view_drawer`

**Menu:** `view_menu`, `edit_menu`, `manage_pricing`, `manage_modifiers`

**Staff:** `view_staff`, `manage_staff`, `edit_schedules`, `approve_timesheets`, `manage_roles`

**Reports:** `view_basic_reports`, `view_financial_reports`, `export_reports`

**Kitchen:** `view_kds`, `manage_stations`, `86_items`

**Tables:** `manage_floor`, `manage_reservations`, `manage_waitlist`

**Inventory:** `view_inventory`, `adjust_stock`, `create_po`, `receive_inventory`

**Customers:** `view_customers`, `manage_loyalty`, `issue_gift_cards`

**Settings:** `manage_integrations`, `manage_tax_rates`, `system_settings`
