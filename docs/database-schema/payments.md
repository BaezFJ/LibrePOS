# Payments Blueprint Schema

> Transactions, tips, discounts, taxes, cash drawer (8 tables)

---

## payment

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *check_id* | INTEGER | FK → check, NOT NULL | |
| amount | DECIMAL(10,2) | NOT NULL | |
| tender_type | VARCHAR(20) | NOT NULL | cash, credit, debit, gift_card, house_account, mobile_wallet |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | pending, authorized, captured, voided, refunded |
| reference_number | VARCHAR(100) | | External reference |
| processor_response | JSONB | | Full response |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| *processed_by_id* | INTEGER | FK → user, NOT NULL | |

---

## tip

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *payment_id* | INTEGER | FK → payment, NOT NULL | |
| amount | DECIMAL(10,2) | NOT NULL | |
| entry_method | VARCHAR(20) | NOT NULL | on_device, adjusted, cash |
| *declared_by_id* | INTEGER | FK → user, NULL | For cash tips |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| adjusted_at | TIMESTAMPTZ | | |

---

## discount

Discount definitions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | |
| discount_type | VARCHAR(20) | NOT NULL | percentage, fixed |
| value | DECIMAL(10,2) | NOT NULL | |
| code | VARCHAR(50) | UNIQUE | Promo code |
| requires_authorization | BOOLEAN | NOT NULL, DEFAULT FALSE | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| start_date | DATE | | |
| end_date | DATE | | |
| usage_limit | INTEGER | | |
| times_used | INTEGER | NOT NULL, DEFAULT 0 | |

---

## applied_discount

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *check_id* | INTEGER | FK → check, NOT NULL | |
| *discount_id* | INTEGER | FK → discount, NOT NULL | |
| amount | DECIMAL(10,2) | NOT NULL | Actual amount |
| *authorized_by_id* | INTEGER | FK → user, NULL | Manager |
| applied_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## tax_rate

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | e.g., 'State Sales Tax' |
| rate | DECIMAL(5,4) | NOT NULL | e.g., 0.0825 = 8.25% |
| jurisdiction | VARCHAR(100) | | |
| applies_to | VARCHAR(20) | NOT NULL, DEFAULT 'all' | food, alcohol, all |
| is_inclusive | BOOLEAN | NOT NULL, DEFAULT FALSE | Tax in price |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |

---

## cash_drawer

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(50) | NOT NULL | |
| station_id | VARCHAR(50) | | POS station |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'closed' | closed, open, counting |
| opened_at | TIMESTAMPTZ | | |
| *opened_by_id* | INTEGER | FK → user, NULL | |
| opening_amount | DECIMAL(10,2) | | |
| current_amount | DECIMAL(10,2) | | |
| expected_amount | DECIMAL(10,2) | | |

---

## cash_drawer_transaction

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *drawer_id* | INTEGER | FK → cash_drawer, NOT NULL | |
| transaction_type | VARCHAR(20) | NOT NULL | sale, paid_in, paid_out, drop |
| amount | DECIMAL(10,2) | NOT NULL | |
| *payment_id* | INTEGER | FK → payment, NULL | |
| notes | TEXT | | |
| *performed_by_id* | INTEGER | FK → user, NOT NULL | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## receipt

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *payment_id* | INTEGER | FK → payment, NOT NULL | |
| receipt_type | VARCHAR(20) | NOT NULL | customer, merchant |
| delivery_method | VARCHAR(20) | NOT NULL | print, email, sms |
| content | TEXT | NOT NULL | |
| delivered_at | TIMESTAMPTZ | | |
| email | VARCHAR(255) | | |
| phone | VARCHAR(20) | | |
