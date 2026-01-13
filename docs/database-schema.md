# Database Schema

PostgreSQL database for LibrePOS Restaurant Point of Sale System.

## Quick Reference

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Table names | lowercase, snake_case, singular | `menu_item`, `order` |
| Primary keys | `id` with SERIAL | `id SERIAL PK` |
| Foreign keys | `referenced_table_id` | `*user_id*`, `*order_id*` |
| Timestamps | TIMESTAMPTZ with timezone | `created_at`, `updated_at` |
| Enums | VARCHAR with CHECK constraints | `status VARCHAR(20)` |
| JSON fields | JSONB type | `config JSONB` |

### Column Notation

- **Bold** (`**id**`): Primary Key
- *Italic* (`*user_id*`): Foreign Key
- `NOT NULL`: Required field
- `DEFAULT value`: Default value if not specified

### Common Column Patterns

```sql
-- Primary key (all tables)
id SERIAL PRIMARY KEY

-- Timestamps (most tables)
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()

-- Soft delete / status
is_active BOOLEAN NOT NULL DEFAULT TRUE
status VARCHAR(20) NOT NULL DEFAULT 'active'

-- Display ordering
display_order INTEGER NOT NULL DEFAULT 0
```

### Blueprint Overview

| Blueprint | Tables | Primary Purpose |
|-----------|--------|-----------------|
| auth | 3 | login_attempt, active_session, api_key |
| menu | 9 | category, menu_item, modifier_group, modifier, menu_item_modifier_group, combo, combo_component, pricing_rule, menu_schedule |
| orders | 5 | order, order_item, order_item_modifier, check, check_item |
| payments | 8 | payment, tip, discount, applied_discount, tax_rate, cash_drawer, cash_drawer_transaction, receipt |
| staff | 9 | user, role, permission, role_permission, time_entry, shift, schedule, tip_declaration, tip_pool_rule |
| kitchen | 6 | station, category_station, kitchen_ticket, kitchen_ticket_item, kitchen_message, prep_time |
| tables | 8 | floor_plan, table, section, table_section, server_section, table_status, reservation, waitlist_entry |
| reporting | 5 | daily_summary, hourly_sales, saved_report, report_execution, audit_log |
| inventory | 8 | inventory_item, stock_level, recipe, recipe_ingredient, vendor, purchase_order, po_line_item, stock_adjustment |
| customers | 5 | customer, loyalty_account, loyalty_tier, gift_card, feedback |
| integrations | 4 | integration, webhook_endpoint, external_order, sync_log |

---

## Auth Blueprint

### login_attempt

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *user_id* | INTEGER | FK → user, NULL | Null if unknown user |
| attempt_time | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| success | BOOLEAN | NOT NULL | |
| ip_address | VARCHAR(45) | NOT NULL | IPv4/IPv6 |
| user_agent | TEXT | | |

### active_session

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *user_id* | INTEGER | FK → user, NOT NULL | |
| session_token | VARCHAR(255) | NOT NULL, UNIQUE | |
| device_info | VARCHAR(255) | | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| expires_at | TIMESTAMPTZ | NOT NULL | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |

### api_key

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | |
| key_hash | VARCHAR(255) | NOT NULL, UNIQUE | Never store plain |
| *user_id* | INTEGER | FK → user, NOT NULL | |
| scopes | JSONB | NOT NULL, DEFAULT '[]' | Permitted API scopes |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| expires_at | TIMESTAMPTZ | | Optional |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| last_used_at | TIMESTAMPTZ | | |

---

## Menu Blueprint

### category

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | |
| description | TEXT | | |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | |
| *parent_id* | INTEGER | FK → category, NULL | For subcategories |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| image_url | VARCHAR(500) | | |

### menu_item

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

### modifier_group

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | e.g., 'Sides', 'Temperature' |
| min_selections | INTEGER | NOT NULL, DEFAULT 0 | |
| max_selections | INTEGER | NOT NULL, DEFAULT 1 | |
| is_required | BOOLEAN | NOT NULL, DEFAULT FALSE | |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | |

### modifier

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | |
| price | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | Additional price |
| *modifier_group_id* | INTEGER | FK → modifier_group, NOT NULL | |
| is_available | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | |

### menu_item_modifier_group

Junction: menu_item ↔ modifier_group

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *menu_item_id* | INTEGER | FK → menu_item, NOT NULL | |
| *modifier_group_id* | INTEGER | FK → modifier_group, NOT NULL | |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | |

### combo

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(150) | NOT NULL | |
| description | TEXT | | |
| price | DECIMAL(10,2) | NOT NULL | Combo price |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| start_date | DATE | | |
| end_date | DATE | | |

### combo_component

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *combo_id* | INTEGER | FK → combo, NOT NULL | |
| *category_id* | INTEGER | FK → category, NOT NULL | Choose from |
| included_quantity | INTEGER | NOT NULL, DEFAULT 1 | |
| display_name | VARCHAR(100) | | Override name |

### pricing_rule

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

### menu_schedule

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

---

## Orders Blueprint

### order

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

### order_item

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

### order_item_modifier

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *order_item_id* | INTEGER | FK → order_item, NOT NULL | |
| *modifier_id* | INTEGER | FK → modifier, NOT NULL | |
| quantity | INTEGER | NOT NULL, DEFAULT 1 | |
| unit_price | DECIMAL(10,2) | NOT NULL | Price at time of order |

### check

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

### check_item

Junction: check ↔ order_item (for split checks).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *check_id* | INTEGER | FK → check, NOT NULL | |
| *order_item_id* | INTEGER | FK → order_item, NOT NULL | |

---

## Payments Blueprint

### payment

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

### tip

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *payment_id* | INTEGER | FK → payment, NOT NULL | |
| amount | DECIMAL(10,2) | NOT NULL | |
| entry_method | VARCHAR(20) | NOT NULL | on_device, adjusted, cash |
| *declared_by_id* | INTEGER | FK → user, NULL | For cash tips |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| adjusted_at | TIMESTAMPTZ | | |

### discount

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

### applied_discount

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *check_id* | INTEGER | FK → check, NOT NULL | |
| *discount_id* | INTEGER | FK → discount, NOT NULL | |
| amount | DECIMAL(10,2) | NOT NULL | Actual amount |
| *authorized_by_id* | INTEGER | FK → user, NULL | Manager |
| applied_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

### tax_rate

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | e.g., 'State Sales Tax' |
| rate | DECIMAL(5,4) | NOT NULL | e.g., 0.0825 = 8.25% |
| jurisdiction | VARCHAR(100) | | |
| applies_to | VARCHAR(20) | NOT NULL, DEFAULT 'all' | food, alcohol, all |
| is_inclusive | BOOLEAN | NOT NULL, DEFAULT FALSE | Tax in price |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |

### cash_drawer

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

### cash_drawer_transaction

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

### receipt

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

---

## Staff Blueprint

### user

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

### role

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(50) | NOT NULL, UNIQUE | |
| description | TEXT | | |
| is_system_role | BOOLEAN | NOT NULL, DEFAULT FALSE | Non-deletable |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

### permission

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| code | VARCHAR(50) | NOT NULL, UNIQUE | e.g., 'void_order' |
| name | VARCHAR(100) | NOT NULL | |
| description | TEXT | | |
| category | VARCHAR(50) | NOT NULL | Grouping |

### role_permission

Junction: role ↔ permission.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *role_id* | INTEGER | FK → role, NOT NULL | |
| *permission_id* | INTEGER | FK → permission, NOT NULL | |

### time_entry

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

### shift

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

### schedule

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | |
| week_start_date | DATE | NOT NULL | Monday |
| is_published | BOOLEAN | NOT NULL, DEFAULT FALSE | |
| published_at | TIMESTAMPTZ | | |
| *created_by_id* | INTEGER | FK → user, NOT NULL | |

### tip_declaration

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

### tip_pool_rule

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | |
| *source_role_id* | INTEGER | FK → role, NOT NULL | Tips out |
| *recipient_role_id* | INTEGER | FK → role, NOT NULL | Receives |
| percentage | DECIMAL(5,2) | NOT NULL | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |

---

## Kitchen Blueprint

### station

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(50) | NOT NULL | |
| station_type | VARCHAR(20) | NOT NULL | grill, fryer, saute, prep, expo, bar, dessert |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| printer_id | VARCHAR(50) | | |

### category_station

Junction: category ↔ station (routing).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *category_id* | INTEGER | FK → category, NOT NULL | |
| *station_id* | INTEGER | FK → station, NOT NULL | |

### kitchen_ticket

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

### kitchen_ticket_item

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *ticket_id* | INTEGER | FK → kitchen_ticket, NOT NULL | |
| *order_item_id* | INTEGER | FK → order_item, NOT NULL | |
| quantity | INTEGER | NOT NULL | |
| notes | TEXT | | |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | pending, cooking, ready |
| position | INTEGER | NOT NULL, DEFAULT 0 | |

### kitchen_message

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *from_user_id* | INTEGER | FK → user, NOT NULL | |
| *to_station_id* | INTEGER | FK → station, NULL | All if null |
| message | TEXT | NOT NULL | |
| is_read | BOOLEAN | NOT NULL, DEFAULT FALSE | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

### prep_time

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *menu_item_id* | INTEGER | FK → menu_item, NOT NULL | |
| *station_id* | INTEGER | FK → station, NOT NULL | |
| average_seconds | INTEGER | NOT NULL | |
| sample_count | INTEGER | NOT NULL, DEFAULT 0 | |
| last_updated | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

---

## Tables Blueprint

### floor_plan

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(100) | NOT NULL | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| is_default | BOOLEAN | NOT NULL, DEFAULT FALSE | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

### table

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

### section

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *floor_plan_id* | INTEGER | FK → floor_plan, NOT NULL | |
| name | VARCHAR(50) | NOT NULL | |
| color | VARCHAR(7) | | Hex color |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

### table_section

Junction: table ↔ section.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *table_id* | INTEGER | FK → table, NOT NULL | |
| *section_id* | INTEGER | FK → section, NOT NULL | |

### server_section

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *user_id* | INTEGER | FK → user, NOT NULL | |
| *section_id* | INTEGER | FK → section, NOT NULL | |
| shift_date | DATE | NOT NULL | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |

### table_status

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

### reservation

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

### waitlist_entry

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

---

## Reporting Blueprint

### daily_summary

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

### hourly_sales

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| business_date | DATE | NOT NULL | |
| hour | INTEGER | NOT NULL | 0-23 |
| sales_amount | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | |
| order_count | INTEGER | NOT NULL, DEFAULT 0 | |
| guest_count | INTEGER | NOT NULL, DEFAULT 0 | |

### saved_report

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

### report_execution

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *saved_report_id* | INTEGER | FK → saved_report, NOT NULL | |
| started_at | TIMESTAMPTZ | NOT NULL | |
| completed_at | TIMESTAMPTZ | | |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'running' | running, completed, failed |
| file_path | VARCHAR(500) | | |
| error_message | TEXT | | |

### audit_log

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

---

## Inventory Blueprint

### inventory_item

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

### stock_level

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *inventory_item_id* | INTEGER | FK → inventory_item, NOT NULL | |
| storage_location | VARCHAR(50) | NOT NULL, DEFAULT 'main' | |
| quantity_on_hand | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | |
| last_counted_at | TIMESTAMPTZ | | |
| last_updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

### recipe

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *menu_item_id* | INTEGER | FK → menu_item, NOT NULL | |
| yield_quantity | DECIMAL(10,2) | NOT NULL, DEFAULT 1 | |
| yield_unit | VARCHAR(20) | NOT NULL, DEFAULT 'serving' | |
| instructions | TEXT | | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |

### recipe_ingredient

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *recipe_id* | INTEGER | FK → recipe, NOT NULL | |
| *inventory_item_id* | INTEGER | FK → inventory_item, NOT NULL | |
| quantity | DECIMAL(10,4) | NOT NULL | |
| unit | VARCHAR(20) | NOT NULL | |
| waste_factor_percent | DECIMAL(5,2) | DEFAULT 0 | |

### vendor

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

### purchase_order

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

### po_line_item

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *purchase_order_id* | INTEGER | FK → purchase_order, NOT NULL | |
| *inventory_item_id* | INTEGER | FK → inventory_item, NOT NULL | |
| quantity_ordered | DECIMAL(10,2) | NOT NULL | |
| unit_cost | DECIMAL(10,4) | NOT NULL | |
| quantity_received | DECIMAL(10,2) | DEFAULT 0 | |
| received_at | TIMESTAMPTZ | | |

### stock_adjustment

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

---

## Customers Blueprint

### customer

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

### loyalty_account

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

### loyalty_tier

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| name | VARCHAR(50) | NOT NULL | Bronze, Silver, Gold |
| min_points | INTEGER | NOT NULL | |
| multiplier | DECIMAL(3,2) | NOT NULL, DEFAULT 1.00 | |
| benefits | JSONB | DEFAULT '[]' | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |

### gift_card

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

### feedback

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

---

## Integrations Blueprint

### integration

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

### webhook_endpoint

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | |
| *integration_id* | INTEGER | FK → integration, NOT NULL | |
| url | VARCHAR(500) | NOT NULL | |
| secret_hash | VARCHAR(255) | | Signing secret |
| events | JSONB | NOT NULL, DEFAULT '[]' | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

### external_order

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

### sync_log

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

---

## Performance Indexes

Beyond primary keys and foreign keys (auto-indexed), add these for query performance:

### Orders & Payments

| Index | Purpose |
|-------|---------|
| `order(status)` | Filter open orders |
| `order(created_at)` | Date range queries |
| `order(server_id, status)` | Server's open orders |
| `order_item(order_id, status)` | Items by order and status |
| `payment(created_at)` | Payment date queries |
| `check(order_id)` | Checks for an order |

### Kitchen & Tables

| Index | Purpose |
|-------|---------|
| `kitchen_ticket(station_id, status)` | Station's pending tickets |
| `kitchen_ticket(created_at)` | Ticket timing |
| `table_status(status)` | Find available tables |
| `reservation(reservation_time)` | By date/time |
| `reservation(status)` | Active reservations |

### Reporting & Analytics

| Index | Purpose |
|-------|---------|
| `daily_summary(business_date)` | Date lookups |
| `hourly_sales(business_date, hour)` | Hourly breakdown |
| `audit_log(created_at)` | Audit trail |
| `audit_log(user_id, created_at)` | User activity |

### Staff & Time

| Index | Purpose |
|-------|---------|
| `user(email)` | Login by email |
| `user(employee_number)` | Lookup by ID |
| `time_entry(user_id, clock_in)` | Employee time records |
| `shift(user_id, scheduled_start)` | Employee schedules |
