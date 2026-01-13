# Menu Blueprint Schema

> Items, categories, modifiers, pricing (9 tables)

---

## category

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | |
| description | TEXT | | |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | |
| *parent_id* | INTEGER | FK → category, NULL | For subcategories |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| image_url | VARCHAR(500) | | |

---

## menu_item

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(150) | NOT NULL | |
| description | TEXT | | |
| price | DECIMAL(10,2) | NOT NULL | Base price |
| *category_id* | INTEGER | FK → category, NOT NULL | |
| sku | VARCHAR(50) | UNIQUE | PLU code |
| image_url | VARCHAR(500) | | |
| is_available | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| is_taxable | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| prep_time_minutes | INTEGER | DEFAULT 15 | |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## modifier_group

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | e.g., 'Sides', 'Temperature' |
| min_selections | INTEGER | NOT NULL, DEFAULT 0 | |
| max_selections | INTEGER | NOT NULL, DEFAULT 1 | |
| is_required | BOOLEAN | NOT NULL, DEFAULT FALSE | |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | |

---

## modifier

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | |
| price | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | Additional price |
| *modifier_group_id* | INTEGER | FK → modifier_group, NOT NULL | |
| is_available | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | |

---

## menu_item_modifier_group

Junction: menu_item ↔ modifier_group

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *menu_item_id* | INTEGER | FK → menu_item, NOT NULL | |
| *modifier_group_id* | INTEGER | FK → modifier_group, NOT NULL | |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | |

---

## combo

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(150) | NOT NULL | |
| description | TEXT | | |
| price | DECIMAL(10,2) | NOT NULL | Combo price |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| start_date | DATE | | |
| end_date | DATE | | |

---

## combo_component

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *combo_id* | INTEGER | FK → combo, NOT NULL | |
| *category_id* | INTEGER | FK → category, NOT NULL | Choose from |
| included_quantity | INTEGER | NOT NULL, DEFAULT 1 | |
| display_name | VARCHAR(100) | | Override name |

---

## pricing_rule

Time-based or conditional pricing (happy hour, daypart).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *menu_item_id* | INTEGER | FK → menu_item, NOT NULL | |
| rule_type | VARCHAR(20) | NOT NULL | happy_hour, daypart, location |
| price | DECIMAL(10,2) | NOT NULL | Override price |
| start_time | TIME | | |
| end_time | TIME | | |
| days_of_week | JSONB | DEFAULT '[]' | [0-6] |
| priority | INTEGER | NOT NULL, DEFAULT 0 | Higher wins |

---

## menu_schedule

Schedule when menu items are available (breakfast, lunch, dinner).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | e.g., 'Breakfast' |
| start_date | DATE | | |
| end_date | DATE | | |
| days_of_week | JSONB | DEFAULT '[]' | |
| start_time | TIME | NOT NULL | |
| end_time | TIME | NOT NULL | |
