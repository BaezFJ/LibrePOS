# Reporting Blueprint Schema

> Sales, analytics, audit logs (5 tables)

---

## daily_summary

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| business_date | DATE | NOT NULL, UNIQUE | |
| gross_sales | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | |
| net_sales | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | |
| tax_collected | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | |
| discounts_given | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | |
| comps_given | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | |
| refunds | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | |
| tips_collected | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | |
| cash_sales | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | |
| credit_sales | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | |
| other_sales | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | |
| order_count | INTEGER | NOT NULL, DEFAULT 0 | |
| guest_count | INTEGER | NOT NULL, DEFAULT 0 | |
| labor_hours | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | |
| labor_cost | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## hourly_sales

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| business_date | DATE | NOT NULL | |
| hour | INTEGER | NOT NULL | 0-23 |
| sales_amount | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | |
| order_count | INTEGER | NOT NULL, DEFAULT 0 | |
| guest_count | INTEGER | NOT NULL, DEFAULT 0 | |

---

## saved_report

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | |
| report_type | VARCHAR(50) | NOT NULL | |
| parameters | JSONB | NOT NULL, DEFAULT '{}' | |
| *created_by_id* | INTEGER | FK → user, NOT NULL | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| is_scheduled | BOOLEAN | NOT NULL, DEFAULT FALSE | |
| schedule_cron | VARCHAR(50) | | |
| email_recipients | JSONB | DEFAULT '[]' | |

---

## report_execution

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *saved_report_id* | INTEGER | FK → saved_report, NOT NULL | |
| started_at | TIMESTAMPTZ | NOT NULL | |
| completed_at | TIMESTAMPTZ | | |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'running' | running, completed, failed |
| file_path | VARCHAR(500) | | |
| error_message | TEXT | | |

---

## audit_log

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *user_id* | INTEGER | FK → user, NOT NULL | |
| action | VARCHAR(50) | NOT NULL | e.g., 'void_order' |
| entity_type | VARCHAR(50) | NOT NULL | |
| entity_id | INTEGER | NOT NULL | |
| old_values | JSONB | | |
| new_values | JSONB | | |
| ip_address | VARCHAR(45) | | |
| user_agent | TEXT | | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
