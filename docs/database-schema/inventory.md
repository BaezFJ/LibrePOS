# Inventory Blueprint Schema

> Stock, recipes, vendors, POs (8 tables)

---

## inventory_item

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(150) | NOT NULL | |
| sku | VARCHAR(50) | UNIQUE | |
| category | VARCHAR(30) | NOT NULL | protein, produce, dairy, dry_goods, beverage, paper, chemical, other |
| unit_of_measure | VARCHAR(20) | NOT NULL | lb, oz, each, case |
| unit_cost | DECIMAL(10,4) | NOT NULL, DEFAULT 0 | |
| par_level | DECIMAL(10,2) | | Target stock |
| reorder_point | DECIMAL(10,2) | | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## stock_level

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *inventory_item_id* | INTEGER | FK → inventory_item, NOT NULL | |
| storage_location | VARCHAR(50) | NOT NULL, DEFAULT 'main' | |
| quantity_on_hand | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | |
| last_counted_at | TIMESTAMPTZ | | |
| last_updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## recipe

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *menu_item_id* | INTEGER | FK → menu_item, NOT NULL | |
| yield_quantity | DECIMAL(10,2) | NOT NULL, DEFAULT 1 | |
| yield_unit | VARCHAR(20) | NOT NULL, DEFAULT 'serving' | |
| instructions | TEXT | | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |

---

## recipe_ingredient

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *recipe_id* | INTEGER | FK → recipe, NOT NULL | |
| *inventory_item_id* | INTEGER | FK → inventory_item, NOT NULL | |
| quantity | DECIMAL(10,4) | NOT NULL | |
| unit | VARCHAR(20) | NOT NULL | |
| waste_factor_percent | DECIMAL(5,2) | DEFAULT 0 | |

---

## vendor

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(150) | NOT NULL | |
| contact_name | VARCHAR(100) | | |
| email | VARCHAR(255) | | |
| phone | VARCHAR(20) | | |
| address | TEXT | | |
| payment_terms | VARCHAR(50) | | e.g., Net 30 |
| lead_time_days | INTEGER | | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| notes | TEXT | | |

---

## purchase_order

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| po_number | VARCHAR(20) | NOT NULL, UNIQUE | |
| *vendor_id* | INTEGER | FK → vendor, NOT NULL | |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'draft' | draft, submitted, confirmed, partial, received, cancelled |
| order_date | DATE | | |
| expected_date | DATE | | |
| received_date | DATE | | |
| subtotal | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | |
| tax | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | |
| total | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | |
| notes | TEXT | | |
| *created_by_id* | INTEGER | FK → user, NOT NULL | |
| *approved_by_id* | INTEGER | FK → user, NULL | |

---

## po_line_item

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *purchase_order_id* | INTEGER | FK → purchase_order, NOT NULL | |
| *inventory_item_id* | INTEGER | FK → inventory_item, NOT NULL | |
| quantity_ordered | DECIMAL(10,2) | NOT NULL | |
| unit_cost | DECIMAL(10,4) | NOT NULL | |
| quantity_received | DECIMAL(10,2) | DEFAULT 0 | |
| received_at | TIMESTAMPTZ | | |

---

## stock_adjustment

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *inventory_item_id* | INTEGER | FK → inventory_item, NOT NULL | |
| adjustment_type | VARCHAR(20) | NOT NULL | count, waste, theft, transfer, received, sold |
| quantity_change | DECIMAL(10,2) | NOT NULL | +/- |
| reason | TEXT | | |
| *performed_by_id* | INTEGER | FK → user, NOT NULL | |
| *approved_by_id* | INTEGER | FK → user, NULL | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
