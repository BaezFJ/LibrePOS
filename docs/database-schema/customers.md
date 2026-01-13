# Customers Blueprint Schema

> Profiles, loyalty, gift cards (5 tables)

---

## customer

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| first_name | VARCHAR(50) | | |
| last_name | VARCHAR(50) | | |
| email | VARCHAR(255) | UNIQUE | |
| phone | VARCHAR(20) | | |
| is_email_verified | BOOLEAN | NOT NULL, DEFAULT FALSE | |
| is_phone_verified | BOOLEAN | NOT NULL, DEFAULT FALSE | |
| marketing_opt_in | BOOLEAN | NOT NULL, DEFAULT FALSE | |
| birthday | DATE | | |
| anniversary | DATE | | |
| notes | TEXT | | |
| tags | JSONB | DEFAULT '[]' | |
| source | VARCHAR(20) | NOT NULL, DEFAULT 'pos' | pos, web, reservation, import |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## loyalty_account

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *customer_id* | INTEGER | FK → customer, NOT NULL, UNIQUE | |
| *tier_id* | INTEGER | FK → loyalty_tier, NOT NULL | |
| points_balance | INTEGER | NOT NULL, DEFAULT 0 | |
| lifetime_points | INTEGER | NOT NULL, DEFAULT 0 | |
| points_expiring | INTEGER | DEFAULT 0 | |
| expiration_date | DATE | | |
| enrolled_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## loyalty_tier

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(50) | NOT NULL | Bronze, Silver, Gold |
| min_points | INTEGER | NOT NULL | |
| multiplier | DECIMAL(3,2) | NOT NULL, DEFAULT 1.00 | |
| benefits | JSONB | DEFAULT '[]' | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |

---

## gift_card

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| card_number | VARCHAR(20) | NOT NULL, UNIQUE | |
| pin_hash | VARCHAR(255) | | |
| initial_balance | DECIMAL(10,2) | NOT NULL | |
| current_balance | DECIMAL(10,2) | NOT NULL | |
| *customer_id* | INTEGER | FK → customer, NULL | Owner |
| *purchased_by_id* | INTEGER | FK → customer, NULL | |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'active' | active, depleted, suspended, expired |
| issued_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| expires_at | DATE | | |

---

## feedback

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *customer_id* | INTEGER | FK → customer, NULL | |
| *order_id* | INTEGER | FK → order, NULL | |
| rating | INTEGER | NOT NULL | 1-5 |
| food_rating | INTEGER | | 1-5 |
| service_rating | INTEGER | | 1-5 |
| ambiance_rating | INTEGER | | 1-5 |
| comment | TEXT | | |
| response | TEXT | | |
| *responded_by_id* | INTEGER | FK → user, NULL | |
| responded_at | TIMESTAMPTZ | | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
