# Orders Blueprint Schema

> Order lifecycle, items, checks (5 tables)

---

## order

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| order_number | VARCHAR(20) | NOT NULL, UNIQUE | Human-readable |
| order_type | VARCHAR(20) | NOT NULL | dine_in, takeout, delivery, bar |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'draft' | draft, submitted, preparing, ready, completed, cancelled |
| *table_id* | INTEGER | FK → table, NULL | Dine-in only |
| *server_id* | INTEGER | FK → user, NOT NULL | |
| *customer_id* | INTEGER | FK → customer, NULL | |
| guest_count | INTEGER | DEFAULT 1 | |
| notes | TEXT | | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| submitted_at | TIMESTAMPTZ | | Sent to kitchen |
| completed_at | TIMESTAMPTZ | | |

---

## order_item

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *order_id* | INTEGER | FK → order, NOT NULL | |
| *menu_item_id* | INTEGER | FK → menu_item, NOT NULL | |
| quantity | INTEGER | NOT NULL, DEFAULT 1 | |
| unit_price | DECIMAL(10,2) | NOT NULL | Price at time of order |
| notes | TEXT | | Special instructions |
| course | VARCHAR(20) | DEFAULT 'entree' | appetizer, entree, dessert, beverage |
| seat_number | INTEGER | | |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | pending, sent, preparing, ready, delivered, voided |
| *voided_by_id* | INTEGER | FK → user, NULL | |
| void_reason | TEXT | | |

---

## order_item_modifier

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *order_item_id* | INTEGER | FK → order_item, NOT NULL | |
| *modifier_id* | INTEGER | FK → modifier, NOT NULL | |
| quantity | INTEGER | NOT NULL, DEFAULT 1 | |
| unit_price | DECIMAL(10,2) | NOT NULL | Price at time of order |

---

## check

Checks/bills for payment (supports split checks).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *order_id* | INTEGER | FK → order, NOT NULL | |
| check_number | INTEGER | NOT NULL | Within order |
| subtotal | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | |
| tax_amount | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | |
| discount_amount | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | |
| total | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'open' | open, paid, partially_paid, voided |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| closed_at | TIMESTAMPTZ | | |

---

## check_item

Junction: check ↔ order_item (for split checks).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *check_id* | INTEGER | FK → check, NOT NULL | |
| *order_item_id* | INTEGER | FK → order_item, NOT NULL | |
