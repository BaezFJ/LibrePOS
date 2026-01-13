# Database Schema

> PostgreSQL database for LibrePOS Restaurant Point of Sale System
> **Total Tables:** 70 across 11 blueprints

---

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Table names | lowercase, snake_case, singular | `menu_item`, `order` |
| Primary keys | `id` with SERIAL | `id SERIAL PK` |
| Foreign keys | `referenced_table_id` | `*user_id*`, `*order_id*` |
| Timestamps | TIMESTAMPTZ with timezone | `created_at`, `updated_at` |
| Enums | VARCHAR with CHECK constraints | `status VARCHAR(20)` |
| JSON fields | JSONB type | `config JSONB` |

---

## Column Notation

- **Bold** (`**id**`): Primary Key
- *Italic* (`*user_id*`): Foreign Key
- `NOT NULL`: Required field
- `DEFAULT value`: Default value if not specified

---

## Common Patterns

```sql
-- Primary key (all tables)
id SERIAL PRIMARY KEY

-- Timestamps (most tables)
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()

-- Soft delete / status
is_active BOOLEAN NOT NULL DEFAULT TRUE
status VARCHAR(20) NOT NULL DEFAULT 'active'

-- Display ordering
display_order INTEGER NOT NULL DEFAULT 0
```

---

## Blueprint Overview

| Blueprint | Tables | Primary Purpose |
|-----------|--------|-----------------|
| [auth](database-schema/auth.md) | 3 | login_attempt, active_session, api_key |
| [menu](database-schema/menu.md) | 9 | category, menu_item, modifier_group, modifier, combo, pricing_rule |
| [orders](database-schema/orders.md) | 5 | order, order_item, order_item_modifier, check, check_item |
| [payments](database-schema/payments.md) | 8 | payment, tip, discount, tax_rate, cash_drawer, receipt |
| [staff](database-schema/staff.md) | 9 | user, role, permission, time_entry, shift, schedule |
| [kitchen](database-schema/kitchen.md) | 6 | station, kitchen_ticket, kitchen_ticket_item, prep_time |
| [tables](database-schema/tables.md) | 8 | floor_plan, table, section, reservation, waitlist_entry |
| [reporting](database-schema/reporting.md) | 5 | daily_summary, hourly_sales, saved_report, audit_log |
| [inventory](database-schema/inventory.md) | 8 | inventory_item, stock_level, recipe, vendor, purchase_order |
| [customers](database-schema/customers.md) | 5 | customer, loyalty_account, loyalty_tier, gift_card, feedback |
| [integrations](database-schema/integrations.md) | 4 | integration, webhook_endpoint, external_order, sync_log |

---

## Key Tables Summary

### Core Operations

| Table | Purpose |
|-------|---------|
| `user` | Staff members, authentication |
| `menu_item` | Products for sale |
| `order` | Customer orders |
| `payment` | Payment transactions |
| `kitchen_ticket` | Kitchen display tickets |

### Supporting Tables

| Table | Purpose |
|-------|---------|
| `category` | Menu organization |
| `modifier` | Item customizations |
| `check` | Split bills |
| `table` | Physical tables |
| `reservation` | Table reservations |

---

## Relationships Overview

```
user ─┬─< order ──< order_item ──< order_item_modifier
      │     │            │
      │     └──< check ──┴──< check_item
      │            │
      │            └──< payment ──< tip
      │
      └──< time_entry
      └──< shift

menu_item ─┬──< order_item
           ├──< recipe ──< recipe_ingredient
           └──< pricing_rule

category ──< menu_item
         └──< category_station ──> station

table ──< table_status
      └──< reservation
```

---

## Performance Indexes

See [indexes.md](database-schema/indexes.md) for recommended indexes by domain.

**Key indexes:**
- `order(status)` - Filter open orders
- `order(server_id, status)` - Server's open orders
- `kitchen_ticket(station_id, status)` - Station's pending tickets
- `table_status(status)` - Find available tables
- `user(email)` - Login by email

---

## Detailed Schema

- [Auth](database-schema/auth.md) - Authentication, sessions, API keys
- [Menu](database-schema/menu.md) - Items, categories, modifiers, pricing
- [Orders](database-schema/orders.md) - Order lifecycle, items, checks
- [Payments](database-schema/payments.md) - Transactions, tips, discounts, taxes
- [Staff](database-schema/staff.md) - Users, roles, permissions, time tracking
- [Kitchen](database-schema/kitchen.md) - KDS, tickets, stations, routing
- [Tables](database-schema/tables.md) - Floor plans, reservations, waitlist
- [Reporting](database-schema/reporting.md) - Sales, analytics, audit logs
- [Inventory](database-schema/inventory.md) - Stock, recipes, vendors, POs
- [Customers](database-schema/customers.md) - Profiles, loyalty, gift cards
- [Integrations](database-schema/integrations.md) - Third-party, webhooks
- [Indexes](database-schema/indexes.md) - Performance indexes
