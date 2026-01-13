# Kitchen Blueprint Schema

> KDS, tickets, stations, routing (6 tables)

---

## station

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(50) | NOT NULL | |
| station_type | VARCHAR(20) | NOT NULL | grill, fryer, saute, prep, expo, bar, dessert |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| printer_id | VARCHAR(50) | | |

---

## category_station

Junction: category ↔ station (routing).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *category_id* | INTEGER | FK → category, NOT NULL | |
| *station_id* | INTEGER | FK → station, NOT NULL | |

---

## kitchen_ticket

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *order_id* | INTEGER | FK → order, NOT NULL | |
| *station_id* | INTEGER | FK → station, NOT NULL | |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | pending, in_progress, ready, bumped, recalled |
| priority | VARCHAR(20) | NOT NULL, DEFAULT 'normal' | normal, rush, vip |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| started_at | TIMESTAMPTZ | | |
| completed_at | TIMESTAMPTZ | | |
| bumped_at | TIMESTAMPTZ | | |
| *bumped_by_id* | INTEGER | FK → user, NULL | |

---

## kitchen_ticket_item

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *ticket_id* | INTEGER | FK → kitchen_ticket, NOT NULL | |
| *order_item_id* | INTEGER | FK → order_item, NOT NULL | |
| quantity | INTEGER | NOT NULL | |
| notes | TEXT | | |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | pending, cooking, ready |
| position | INTEGER | NOT NULL, DEFAULT 0 | |

---

## kitchen_message

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *from_user_id* | INTEGER | FK → user, NOT NULL | |
| *to_station_id* | INTEGER | FK → station, NULL | All if null |
| message | TEXT | NOT NULL | |
| is_read | BOOLEAN | NOT NULL, DEFAULT FALSE | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## prep_time

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *menu_item_id* | INTEGER | FK → menu_item, NOT NULL | |
| *station_id* | INTEGER | FK → station, NOT NULL | |
| average_seconds | INTEGER | NOT NULL | |
| sample_count | INTEGER | NOT NULL, DEFAULT 0 | |
| last_updated | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
