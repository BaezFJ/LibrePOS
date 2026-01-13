# Integrations Blueprint Schema

> Third-party, webhooks, external orders (4 tables)

---

## integration

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | |
| integration_type | VARCHAR(30) | NOT NULL | delivery, accounting, payroll, reservation, marketing, payment |
| provider | VARCHAR(50) | NOT NULL | DoorDash, QuickBooks, etc. |
| is_active | BOOLEAN | NOT NULL, DEFAULT FALSE | |
| config | JSONB | NOT NULL, DEFAULT '{}' | Encrypted |
| credentials | JSONB | NOT NULL, DEFAULT '{}' | Encrypted |
| last_sync_at | TIMESTAMPTZ | | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## webhook_endpoint

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *integration_id* | INTEGER | FK → integration, NOT NULL | |
| url | VARCHAR(500) | NOT NULL | |
| secret_hash | VARCHAR(255) | | Signing secret |
| events | JSONB | NOT NULL, DEFAULT '[]' | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## external_order

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *integration_id* | INTEGER | FK → integration, NOT NULL | |
| external_id | VARCHAR(100) | NOT NULL | |
| *order_id* | INTEGER | FK → order, NULL | Linked POS order |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'received' | received, accepted, rejected, preparing, ready, picked_up, delivered, cancelled |
| external_status | VARCHAR(50) | | |
| raw_data | JSONB | NOT NULL | |
| received_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| synced_at | TIMESTAMPTZ | | |

---

## sync_log

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *integration_id* | INTEGER | FK → integration, NOT NULL | |
| sync_type | VARCHAR(50) | NOT NULL | |
| direction | VARCHAR(10) | NOT NULL | inbound, outbound |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'started' | started, completed, failed |
| records_processed | INTEGER | DEFAULT 0 | |
| errors | JSONB | DEFAULT '[]' | |
| started_at | TIMESTAMPTZ | NOT NULL | |
| completed_at | TIMESTAMPTZ | | |
