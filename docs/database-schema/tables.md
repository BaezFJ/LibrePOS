# Tables Blueprint Schema

> Floor plans, tables, reservations, waitlist (8 tables)

---

## floor_plan

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| is_default | BOOLEAN | NOT NULL, DEFAULT FALSE | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *floor_plan_id* | INTEGER | FK → floor_plan, NOT NULL | |
| table_number | VARCHAR(10) | NOT NULL | |
| name | VARCHAR(50) | | |
| capacity_min | INTEGER | NOT NULL, DEFAULT 1 | |
| capacity_max | INTEGER | NOT NULL | |
| x_position | INTEGER | NOT NULL, DEFAULT 0 | |
| y_position | INTEGER | NOT NULL, DEFAULT 0 | |
| width | INTEGER | NOT NULL, DEFAULT 100 | |
| height | INTEGER | NOT NULL, DEFAULT 100 | |
| shape | VARCHAR(20) | NOT NULL, DEFAULT 'square' | square, rectangle, round, oval |
| rotation | INTEGER | NOT NULL, DEFAULT 0 | Degrees |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| is_combinable | BOOLEAN | NOT NULL, DEFAULT TRUE | |

---

## section

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *floor_plan_id* | INTEGER | FK → floor_plan, NOT NULL | |
| name | VARCHAR(50) | NOT NULL | |
| color | VARCHAR(7) | | Hex color |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## table_section

Junction: table ↔ section.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *table_id* | INTEGER | FK → table, NOT NULL | |
| *section_id* | INTEGER | FK → section, NOT NULL | |

---

## server_section

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *user_id* | INTEGER | FK → user, NOT NULL | |
| *section_id* | INTEGER | FK → section, NOT NULL | |
| shift_date | DATE | NOT NULL | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |

---

## table_status

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *table_id* | INTEGER | FK → table, NOT NULL, UNIQUE | |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'available' | available, reserved, seated, ordered, entrees_dropped, dessert, check_presented, paid, dirty, blocked |
| party_size | INTEGER | | |
| *server_id* | INTEGER | FK → user, NULL | |
| *order_id* | INTEGER | FK → order, NULL | |
| seated_at | TIMESTAMPTZ | | |
| status_changed_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## reservation

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| customer_name | VARCHAR(100) | NOT NULL | |
| phone | VARCHAR(20) | | |
| email | VARCHAR(255) | | |
| *customer_id* | INTEGER | FK → customer, NULL | |
| party_size | INTEGER | NOT NULL | |
| reservation_time | TIMESTAMPTZ | NOT NULL | |
| *table_id* | INTEGER | FK → table, NULL | Pre-assigned |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'booked' | booked, confirmed, seated, completed, no_show, cancelled |
| notes | TEXT | | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| confirmed_at | TIMESTAMPTZ | | |
| source | VARCHAR(20) | NOT NULL, DEFAULT 'phone' | phone, web, third_party |

---

## waitlist_entry

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| customer_name | VARCHAR(100) | NOT NULL | |
| phone | VARCHAR(20) | | |
| party_size | INTEGER | NOT NULL | |
| quoted_wait_minutes | INTEGER | | |
| check_in_time | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| notified_at | TIMESTAMPTZ | | |
| seated_at | TIMESTAMPTZ | | |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'waiting' | waiting, notified, seated, left, removed |
| notes | TEXT | | |
