# Staff Blueprint Schema

> Users, roles, permissions, time tracking (9 tables)

---

## user

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| employee_number | VARCHAR(20) | UNIQUE | |
| first_name | VARCHAR(50) | NOT NULL | |
| last_name | VARCHAR(50) | NOT NULL | |
| email | VARCHAR(255) | UNIQUE | |
| phone | VARCHAR(20) | | |
| pin_hash | VARCHAR(255) | | Quick login |
| password_hash | VARCHAR(255) | | |
| *role_id* | INTEGER | FK → role, NOT NULL | |
| hire_date | DATE | | |
| termination_date | DATE | | |
| hourly_rate | DECIMAL(10,2) | | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## role

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(50) | NOT NULL, UNIQUE | |
| description | TEXT | | |
| is_system_role | BOOLEAN | NOT NULL, DEFAULT FALSE | Non-deletable |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## permission

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| code | VARCHAR(50) | NOT NULL, UNIQUE | e.g., 'void_order' |
| name | VARCHAR(100) | NOT NULL | |
| description | TEXT | | |
| category | VARCHAR(50) | NOT NULL | Grouping |

---

## role_permission

Junction: role ↔ permission.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *role_id* | INTEGER | FK → role, NOT NULL | |
| *permission_id* | INTEGER | FK → permission, NOT NULL | |

---

## time_entry

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *user_id* | INTEGER | FK → user, NOT NULL | |
| clock_in | TIMESTAMPTZ | NOT NULL | |
| clock_out | TIMESTAMPTZ | | |
| break_minutes | INTEGER | DEFAULT 0 | |
| *shift_id* | INTEGER | FK → shift, NULL | |
| is_edited | BOOLEAN | NOT NULL, DEFAULT FALSE | |
| *edited_by_id* | INTEGER | FK → user, NULL | |
| edit_reason | TEXT | | |
| original_clock_in | TIMESTAMPTZ | | |
| original_clock_out | TIMESTAMPTZ | | |

---

## shift

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *user_id* | INTEGER | FK → user, NOT NULL | |
| scheduled_start | TIMESTAMPTZ | NOT NULL | |
| scheduled_end | TIMESTAMPTZ | NOT NULL | |
| actual_start | TIMESTAMPTZ | | |
| actual_end | TIMESTAMPTZ | | |
| *role_id* | INTEGER | FK → role, NOT NULL | Role for shift |
| notes | TEXT | | |

---

## schedule

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | |
| week_start_date | DATE | NOT NULL | Monday |
| is_published | BOOLEAN | NOT NULL, DEFAULT FALSE | |
| published_at | TIMESTAMPTZ | | |
| *created_by_id* | INTEGER | FK → user, NOT NULL | |

---

## tip_declaration

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *user_id* | INTEGER | FK → user, NOT NULL | |
| shift_date | DATE | NOT NULL | |
| cash_tips | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | |
| credit_tips | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | |
| tip_out_given | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | |
| tip_out_received | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | |
| declared_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## tip_pool_rule

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | |
| *source_role_id* | INTEGER | FK → role, NOT NULL | Tips out |
| *recipient_role_id* | INTEGER | FK → role, NOT NULL | Receives |
| percentage | DECIMAL(5,2) | NOT NULL | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
