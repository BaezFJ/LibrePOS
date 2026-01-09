# Database Schema Document

## Restaurant Point of Sale System

**Version 1.0 | January 2026**

*PostgreSQL Database*

---

## Document Legend

| Highlight | Description |
|-----------|-------------|
| Yellow Row | Primary Key column |
| Blue Row | Foreign Key column |

---

## 1. Overview

This document defines the complete database schema for the Restaurant POS System. The schema is organized by blueprint/module, with each section containing table definitions, column specifications, constraints, and relationships.

The database uses PostgreSQL with the following conventions:

- **Table names**: lowercase, snake_case, singular (e.g., `menu_item`, `order`)
- **Primary keys**: `id` column with SERIAL (auto-increment)
- **Foreign keys**: `referenced_table_id` naming convention
- **Timestamps**: `created_at`, `updated_at` with timezone
- **Enums**: Implemented as VARCHAR with CHECK constraints
- **JSON fields**: JSONB type for flexible data storage

### 1.1 Table Summary by Blueprint

| Blueprint | Tables | Primary Tables |
|-----------|--------|----------------|
| auth | 3 | login_attempt, active_session, api_key |
| menu | 8 | category, menu_item, modifier_group, modifier, combo, pricing_rule, menu_schedule |
| orders | 5 | order, order_item, order_item_modifier, check, check_item |
| payments | 8 | payment, tip, discount, applied_discount, tax_rate, cash_drawer, cash_drawer_transaction, receipt |
| staff | 8 | user, role, permission, role_permission, time_entry, shift, schedule, tip_declaration, tip_pool_rule |
| kitchen | 6 | station, category_station, kitchen_ticket, kitchen_ticket_item, kitchen_message, prep_time |
| tables | 8 | floor_plan, table, section, table_section, server_section, table_status, reservation, waitlist_entry |
| reporting | 4 | daily_summary, hourly_sales, saved_report, report_execution, audit_log |
| inventory | 10 | inventory_item, unit_conversion, stock_level, recipe, recipe_ingredient, stock_adjustment, vendor, vendor_item, purchase_order, po_line_item, receiving_log |
| customers | 10 | customer, customer_preference, customer_allergy, loyalty_tier, loyalty_account, loyalty_transaction, reward, reward_redemption, gift_card, gift_card_transaction, feedback |
| integrations | 5 | integration, webhook_endpoint, webhook_log, external_order, sync_log |

---

## 2. Auth Blueprint Tables

### 2.1 login_attempt

Tracks all login attempts for security monitoring and brute-force prevention.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *user_id* | INTEGER | FK, NULL | Reference to user (null if unknown) |
| attempt_time | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | When the attempt occurred |
| success | BOOLEAN | NOT NULL | Whether login was successful |
| ip_address | VARCHAR(45) | NOT NULL | Client IP address (IPv4/IPv6) |
| user_agent | TEXT | | Browser/client user agent string |

### 2.2 active_session

Manages active user sessions for session-based authentication.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *user_id* | INTEGER | FK, NOT NULL | Reference to user |
| session_token | VARCHAR(255) | NOT NULL, UNIQUE | Secure session token |
| device_info | VARCHAR(255) | | Device/browser information |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Session creation time |
| expires_at | TIMESTAMPTZ | NOT NULL | Session expiration time |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Whether session is active |

### 2.3 api_key

Stores API keys for third-party integrations and programmatic access.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Descriptive name for the API key |
| key_hash | VARCHAR(255) | NOT NULL, UNIQUE | Hashed API key (never store plain) |
| *user_id* | INTEGER | FK, NOT NULL | User who owns the key |
| scopes | JSONB | NOT NULL, DEFAULT '[]' | Permitted API scopes/permissions |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Key creation time |
| expires_at | TIMESTAMPTZ | | Optional expiration date |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Whether key is active |
| last_used_at | TIMESTAMPTZ | | Last time key was used |

---

## 3. Menu Blueprint Tables

### 3.1 category

Menu categories for organizing items (e.g., Appetizers, Entrees, Beverages).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Category name |
| description | TEXT | | Optional description |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | Sort order for display |
| *parent_id* | INTEGER | FK, NULL | Parent category (for subcategories) |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Whether category is visible |
| image_url | VARCHAR(500) | | Category image URL |

### 3.2 menu_item

Individual menu items available for ordering.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(150) | NOT NULL | Item name |
| description | TEXT | | Item description |
| price | DECIMAL(10,2) | NOT NULL | Base price |
| *category_id* | INTEGER | FK, NOT NULL | Parent category |
| sku | VARCHAR(50) | UNIQUE | Stock keeping unit / PLU code |
| image_url | VARCHAR(500) | | Item image URL |
| is_available | BOOLEAN | NOT NULL, DEFAULT TRUE | Currently available for order |
| is_taxable | BOOLEAN | NOT NULL, DEFAULT TRUE | Whether item is taxed |
| prep_time_minutes | INTEGER | DEFAULT 15 | Estimated preparation time |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | Sort order within category |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Record creation time |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update time |

### 3.3 modifier_group

Groups of modifiers (e.g., 'Choose a Side', 'Select Temperature').

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Group name (e.g., 'Sides') |
| min_selections | INTEGER | NOT NULL, DEFAULT 0 | Minimum required selections |
| max_selections | INTEGER | NOT NULL, DEFAULT 1 | Maximum allowed selections |
| is_required | BOOLEAN | NOT NULL, DEFAULT FALSE | Must select at least min |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | Sort order |

### 3.4 modifier

Individual modifiers within a modifier group.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Modifier name |
| price | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | Additional price |
| *modifier_group_id* | INTEGER | FK, NOT NULL | Parent modifier group |
| is_available | BOOLEAN | NOT NULL, DEFAULT TRUE | Currently available |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | Sort order within group |

### 3.5 menu_item_modifier_group

Junction table linking menu items to their available modifier groups.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *menu_item_id* | INTEGER | FK, NOT NULL | Reference to menu item |
| *modifier_group_id* | INTEGER | FK, NOT NULL | Reference to modifier group |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | Order to show modifier groups |

### 3.6 combo

Combo meals with bundled pricing.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(150) | NOT NULL | Combo name |
| description | TEXT | | Combo description |
| price | DECIMAL(10,2) | NOT NULL | Combo price |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Currently available |
| start_date | DATE | | Optional start date |
| end_date | DATE | | Optional end date |

### 3.7 combo_component

Components that make up a combo (choose from category).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *combo_id* | INTEGER | FK, NOT NULL | Parent combo |
| *category_id* | INTEGER | FK, NOT NULL | Category to choose from |
| included_quantity | INTEGER | NOT NULL, DEFAULT 1 | How many items included |
| display_name | VARCHAR(100) | | Override display name |

### 3.8 pricing_rule

Time-based or conditional pricing rules (happy hour, daypart).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *menu_item_id* | INTEGER | FK, NOT NULL | Item this rule applies to |
| rule_type | VARCHAR(20) | NOT NULL | Type: happy_hour, daypart, location |
| price | DECIMAL(10,2) | NOT NULL | Override price when rule applies |
| start_time | TIME | | Daily start time |
| end_time | TIME | | Daily end time |
| days_of_week | JSONB | DEFAULT '[]' | Days rule applies [0-6] |
| priority | INTEGER | NOT NULL, DEFAULT 0 | Higher priority rules win |

### 3.9 menu_schedule

Schedule when certain menu items are available (breakfast, lunch, dinner menus).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Schedule name (e.g., 'Breakfast') |
| start_date | DATE | | Optional date range start |
| end_date | DATE | | Optional date range end |
| days_of_week | JSONB | DEFAULT '[]' | Days schedule applies |
| start_time | TIME | NOT NULL | Daily start time |
| end_time | TIME | NOT NULL | Daily end time |

---

## 4. Orders Blueprint Tables

### 4.1 order

Core order records containing all order information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| order_number | VARCHAR(20) | NOT NULL, UNIQUE | Human-readable order number |
| order_type | VARCHAR(20) | NOT NULL | dine_in, takeout, delivery, bar |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'draft' | draft, submitted, preparing, ready, completed, cancelled |
| *table_id* | INTEGER | FK, NULL | Table reference (dine-in only) |
| *server_id* | INTEGER | FK, NOT NULL | Server who owns order |
| *customer_id* | INTEGER | FK, NULL | Optional customer reference |
| guest_count | INTEGER | DEFAULT 1 | Number of guests |
| notes | TEXT | | Order-level notes |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Order creation time |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update time |
| submitted_at | TIMESTAMPTZ | | When sent to kitchen |
| completed_at | TIMESTAMPTZ | | When order completed |

### 4.2 order_item

Individual line items within an order.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *order_id* | INTEGER | FK, NOT NULL | Parent order |
| *menu_item_id* | INTEGER | FK, NOT NULL | Menu item ordered |
| quantity | INTEGER | NOT NULL, DEFAULT 1 | Quantity ordered |
| unit_price | DECIMAL(10,2) | NOT NULL | Price at time of order |
| notes | TEXT | | Special instructions |
| course | VARCHAR(20) | DEFAULT 'entree' | appetizer, entree, dessert, beverage |
| seat_number | INTEGER | | Guest seat for item |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | pending, sent, preparing, ready, delivered, voided |
| *voided_by_id* | INTEGER | FK, NULL | User who voided item |
| void_reason | TEXT | | Reason for void |

### 4.3 order_item_modifier

Modifiers applied to order items.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *order_item_id* | INTEGER | FK, NOT NULL | Parent order item |
| *modifier_id* | INTEGER | FK, NOT NULL | Modifier applied |
| quantity | INTEGER | NOT NULL, DEFAULT 1 | Modifier quantity |
| unit_price | DECIMAL(10,2) | NOT NULL | Price at time of order |

### 4.4 check

Checks/bills for payment (supports split checks).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *order_id* | INTEGER | FK, NOT NULL | Parent order |
| check_number | INTEGER | NOT NULL | Check number within order |
| subtotal | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | Pre-tax subtotal |
| tax_amount | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | Total tax |
| discount_amount | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | Total discounts |
| total | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | Final total |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'open' | open, paid, partially_paid, voided |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Check creation time |
| closed_at | TIMESTAMPTZ | | When check was closed |

### 4.5 check_item

Links order items to checks for split check support.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *check_id* | INTEGER | FK, NOT NULL | Parent check |
| *order_item_id* | INTEGER | FK, NOT NULL | Order item on this check |

---

## 5. Payments Blueprint Tables

### 5.1 payment

Payment transactions against checks.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *check_id* | INTEGER | FK, NOT NULL | Check being paid |
| amount | DECIMAL(10,2) | NOT NULL | Payment amount |
| tender_type | VARCHAR(20) | NOT NULL | cash, credit, debit, gift_card, house_account, mobile_wallet |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | pending, authorized, captured, voided, refunded |
| reference_number | VARCHAR(100) | | External transaction reference |
| processor_response | JSONB | | Full processor response |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Payment time |
| *processed_by_id* | INTEGER | FK, NOT NULL | User who processed payment |

### 5.2 tip

Tips associated with payments.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *payment_id* | INTEGER | FK, NOT NULL | Associated payment |
| amount | DECIMAL(10,2) | NOT NULL | Tip amount |
| entry_method | VARCHAR(20) | NOT NULL | on_device, adjusted, cash |
| *declared_by_id* | INTEGER | FK, NULL | User who declared (for cash tips) |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Initial entry time |
| adjusted_at | TIMESTAMPTZ | | When tip was adjusted |

### 5.3 discount

Discount definitions available in the system.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Discount name |
| discount_type | VARCHAR(20) | NOT NULL | percentage, fixed |
| value | DECIMAL(10,2) | NOT NULL | Percentage or fixed amount |
| code | VARCHAR(50) | UNIQUE | Promo code (optional) |
| requires_authorization | BOOLEAN | NOT NULL, DEFAULT FALSE | Needs manager approval |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Currently available |
| start_date | DATE | | Validity start |
| end_date | DATE | | Validity end |
| usage_limit | INTEGER | | Max times can be used |
| times_used | INTEGER | NOT NULL, DEFAULT 0 | Times used so far |

### 5.4 applied_discount

Record of discounts applied to checks.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *check_id* | INTEGER | FK, NOT NULL | Check discount applied to |
| *discount_id* | INTEGER | FK, NOT NULL | Discount that was applied |
| amount | DECIMAL(10,2) | NOT NULL | Actual amount discounted |
| *authorized_by_id* | INTEGER | FK, NULL | Manager who authorized |
| applied_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | When applied |

### 5.5 tax_rate

Tax rate configurations by jurisdiction and type.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Tax name (e.g., 'State Sales Tax') |
| rate | DECIMAL(5,4) | NOT NULL | Tax rate (e.g., 0.0825 for 8.25%) |
| jurisdiction | VARCHAR(100) | | Geographic jurisdiction |
| applies_to | VARCHAR(20) | NOT NULL, DEFAULT 'all' | food, alcohol, all |
| is_inclusive | BOOLEAN | NOT NULL, DEFAULT FALSE | Tax included in price |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Currently active |

### 5.6 cash_drawer

Cash drawer status and balances.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(50) | NOT NULL | Drawer name/identifier |
| station_id | VARCHAR(50) | | POS station identifier |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'closed' | closed, open, counting |
| opened_at | TIMESTAMPTZ | | When drawer was opened |
| *opened_by_id* | INTEGER | FK, NULL | User who opened drawer |
| opening_amount | DECIMAL(10,2) | | Starting cash amount |
| current_amount | DECIMAL(10,2) | | Current calculated amount |
| expected_amount | DECIMAL(10,2) | | Expected based on transactions |

### 5.7 cash_drawer_transaction

All transactions affecting cash drawer balance.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *drawer_id* | INTEGER | FK, NOT NULL | Cash drawer |
| transaction_type | VARCHAR(20) | NOT NULL | sale, paid_in, paid_out, drop |
| amount | DECIMAL(10,2) | NOT NULL | Transaction amount |
| *payment_id* | INTEGER | FK, NULL | Related payment (for sales) |
| notes | TEXT | | Transaction notes |
| *performed_by_id* | INTEGER | FK, NOT NULL | User who performed action |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Transaction time |

### 5.8 receipt

Receipt generation and delivery records.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *payment_id* | INTEGER | FK, NOT NULL | Associated payment |
| receipt_type | VARCHAR(20) | NOT NULL | customer, merchant |
| delivery_method | VARCHAR(20) | NOT NULL | print, email, sms |
| content | TEXT | NOT NULL | Receipt content/template |
| delivered_at | TIMESTAMPTZ | | When delivered |
| email | VARCHAR(255) | | Email address if emailed |
| phone | VARCHAR(20) | | Phone if SMS |

---

## 6. Staff Blueprint Tables

### 6.1 user

Employee/user accounts for all system access.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| employee_number | VARCHAR(20) | UNIQUE | Employee ID number |
| first_name | VARCHAR(50) | NOT NULL | First name |
| last_name | VARCHAR(50) | NOT NULL | Last name |
| email | VARCHAR(255) | UNIQUE | Email address |
| phone | VARCHAR(20) | | Phone number |
| pin_hash | VARCHAR(255) | | Hashed PIN for quick login |
| password_hash | VARCHAR(255) | | Hashed password |
| *role_id* | INTEGER | FK, NOT NULL | User's role |
| hire_date | DATE | | Date of hire |
| termination_date | DATE | | Date of termination |
| hourly_rate | DECIMAL(10,2) | | Pay rate |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Active employee |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Record creation |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update |

### 6.2 role

User roles defining permission sets.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(50) | NOT NULL, UNIQUE | Role name |
| description | TEXT | | Role description |
| is_system_role | BOOLEAN | NOT NULL, DEFAULT FALSE | System-defined (non-deletable) |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation time |

### 6.3 permission

Individual permissions that can be assigned to roles.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| code | VARCHAR(50) | NOT NULL, UNIQUE | Permission code (e.g., 'void_order') |
| name | VARCHAR(100) | NOT NULL | Display name |
| description | TEXT | | What this permission allows |
| category | VARCHAR(50) | NOT NULL | Grouping category |

### 6.4 role_permission

Junction table assigning permissions to roles.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *role_id* | INTEGER | FK, NOT NULL | Role |
| *permission_id* | INTEGER | FK, NOT NULL | Permission |

### 6.5 time_entry

Clock in/out records for time tracking.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *user_id* | INTEGER | FK, NOT NULL | Employee |
| clock_in | TIMESTAMPTZ | NOT NULL | Clock in time |
| clock_out | TIMESTAMPTZ | | Clock out time |
| break_minutes | INTEGER | DEFAULT 0 | Total break time |
| *shift_id* | INTEGER | FK, NULL | Associated scheduled shift |
| is_edited | BOOLEAN | NOT NULL, DEFAULT FALSE | Was manually edited |
| *edited_by_id* | INTEGER | FK, NULL | Manager who edited |
| edit_reason | TEXT | | Reason for edit |
| original_clock_in | TIMESTAMPTZ | | Original time if edited |
| original_clock_out | TIMESTAMPTZ | | Original time if edited |

### 6.6 shift

Scheduled and actual shift records.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *user_id* | INTEGER | FK, NOT NULL | Employee assigned |
| scheduled_start | TIMESTAMPTZ | NOT NULL | Scheduled start time |
| scheduled_end | TIMESTAMPTZ | NOT NULL | Scheduled end time |
| actual_start | TIMESTAMPTZ | | Actual start time |
| actual_end | TIMESTAMPTZ | | Actual end time |
| *role_id* | INTEGER | FK, NOT NULL | Role for this shift |
| notes | TEXT | | Shift notes |

### 6.7 schedule

Weekly schedule containers.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Schedule name |
| week_start_date | DATE | NOT NULL | Monday of the week |
| is_published | BOOLEAN | NOT NULL, DEFAULT FALSE | Visible to staff |
| published_at | TIMESTAMPTZ | | When published |
| *created_by_id* | INTEGER | FK, NOT NULL | Manager who created |

### 6.8 tip_declaration

Daily tip declarations by employees.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *user_id* | INTEGER | FK, NOT NULL | Employee declaring |
| shift_date | DATE | NOT NULL | Date of shift |
| cash_tips | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | Cash tips received |
| credit_tips | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | Credit card tips |
| tip_out_given | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | Tips given to support |
| tip_out_received | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | Tips from pool |
| declared_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Declaration time |

### 6.9 tip_pool_rule

Rules for tip pooling between roles.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Rule name |
| *source_role_id* | INTEGER | FK, NOT NULL | Role that tips out |
| *recipient_role_id* | INTEGER | FK, NOT NULL | Role that receives |
| percentage | DECIMAL(5,2) | NOT NULL | Percentage of tips |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Rule is active |

---

## 7. Kitchen Blueprint Tables

### 7.1 station

Kitchen stations/lines for ticket routing.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(50) | NOT NULL | Station name |
| station_type | VARCHAR(20) | NOT NULL | grill, fryer, saute, prep, expo, bar, dessert |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | Order on KDS |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Station is active |
| printer_id | VARCHAR(50) | | Associated printer ID |

### 7.2 category_station

Maps menu categories to kitchen stations for routing.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *category_id* | INTEGER | FK, NOT NULL | Menu category |
| *station_id* | INTEGER | FK, NOT NULL | Kitchen station |

### 7.3 kitchen_ticket

Tickets sent to kitchen stations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *order_id* | INTEGER | FK, NOT NULL | Source order |
| *station_id* | INTEGER | FK, NOT NULL | Target station |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | pending, in_progress, ready, bumped, recalled |
| priority | VARCHAR(20) | NOT NULL, DEFAULT 'normal' | normal, rush, vip |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Ticket creation time |
| started_at | TIMESTAMPTZ | | When cooking started |
| completed_at | TIMESTAMPTZ | | When cooking finished |
| bumped_at | TIMESTAMPTZ | | When bumped/completed |
| *bumped_by_id* | INTEGER | FK, NULL | User who bumped |

### 7.4 kitchen_ticket_item

Items on a kitchen ticket.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *ticket_id* | INTEGER | FK, NOT NULL | Parent ticket |
| *order_item_id* | INTEGER | FK, NOT NULL | Order item reference |
| quantity | INTEGER | NOT NULL | Quantity to make |
| notes | TEXT | | Special instructions |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | pending, cooking, ready |
| position | INTEGER | NOT NULL, DEFAULT 0 | Display position on ticket |

### 7.5 kitchen_message

Messages between kitchen and front of house.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *from_user_id* | INTEGER | FK, NOT NULL | Message sender |
| *to_station_id* | INTEGER | FK, NULL | Target station (or all if null) |
| message | TEXT | NOT NULL | Message content |
| is_read | BOOLEAN | NOT NULL, DEFAULT FALSE | Has been read |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Message time |

### 7.6 prep_time

Tracked prep times for items at stations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *menu_item_id* | INTEGER | FK, NOT NULL | Menu item |
| *station_id* | INTEGER | FK, NOT NULL | Station |
| average_seconds | INTEGER | NOT NULL | Average prep time |
| sample_count | INTEGER | NOT NULL, DEFAULT 0 | Number of samples |
| last_updated | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last calculation time |

---

## 8. Tables Blueprint Tables

### 8.1 floor_plan

Floor plan layouts for the restaurant.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Floor plan name |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Currently in use |
| is_default | BOOLEAN | NOT NULL, DEFAULT FALSE | Default floor plan |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation time |

### 8.2 table

Individual tables with positioning and properties.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *floor_plan_id* | INTEGER | FK, NOT NULL | Parent floor plan |
| table_number | VARCHAR(10) | NOT NULL | Table number/name |
| name | VARCHAR(50) | | Optional display name |
| capacity_min | INTEGER | NOT NULL, DEFAULT 1 | Minimum seating |
| capacity_max | INTEGER | NOT NULL | Maximum seating |
| x_position | INTEGER | NOT NULL, DEFAULT 0 | X coordinate on floor plan |
| y_position | INTEGER | NOT NULL, DEFAULT 0 | Y coordinate on floor plan |
| width | INTEGER | NOT NULL, DEFAULT 100 | Table width in pixels |
| height | INTEGER | NOT NULL, DEFAULT 100 | Table height in pixels |
| shape | VARCHAR(20) | NOT NULL, DEFAULT 'square' | square, rectangle, round, oval |
| rotation | INTEGER | NOT NULL, DEFAULT 0 | Rotation in degrees |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Table is available |
| is_combinable | BOOLEAN | NOT NULL, DEFAULT TRUE | Can be combined with others |

### 8.3 section

Server sections grouping tables.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *floor_plan_id* | INTEGER | FK, NOT NULL | Parent floor plan |
| name | VARCHAR(50) | NOT NULL | Section name |
| color | VARCHAR(7) | | Hex color for display |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation time |

### 8.4 table_section

Assigns tables to sections.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *table_id* | INTEGER | FK, NOT NULL | Table |
| *section_id* | INTEGER | FK, NOT NULL | Section |

### 8.5 server_section

Assigns servers to sections for a shift.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *user_id* | INTEGER | FK, NOT NULL | Server |
| *section_id* | INTEGER | FK, NOT NULL | Section assigned |
| shift_date | DATE | NOT NULL | Date of assignment |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Currently active |

### 8.6 table_status

Current status of each table.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *table_id* | INTEGER | FK, NOT NULL, UNIQUE | Table reference |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'available' | available, reserved, seated, ordered, entrees_dropped, dessert, check_presented, paid, dirty, blocked |
| party_size | INTEGER | | Current party size |
| *server_id* | INTEGER | FK, NULL | Assigned server |
| *order_id* | INTEGER | FK, NULL | Current order |
| seated_at | TIMESTAMPTZ | | When party was seated |
| status_changed_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last status change |

### 8.7 reservation

Table reservations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| customer_name | VARCHAR(100) | NOT NULL | Guest name |
| phone | VARCHAR(20) | | Contact phone |
| email | VARCHAR(255) | | Contact email |
| *customer_id* | INTEGER | FK, NULL | Linked customer profile |
| party_size | INTEGER | NOT NULL | Number of guests |
| reservation_time | TIMESTAMPTZ | NOT NULL | Reservation date/time |
| *table_id* | INTEGER | FK, NULL | Pre-assigned table |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'booked' | booked, confirmed, seated, completed, no_show, cancelled |
| notes | TEXT | | Special requests |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Booking time |
| confirmed_at | TIMESTAMPTZ | | Confirmation time |
| source | VARCHAR(20) | NOT NULL, DEFAULT 'phone' | phone, web, third_party |

### 8.8 waitlist_entry

Walk-in waitlist entries.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| customer_name | VARCHAR(100) | NOT NULL | Guest name |
| phone | VARCHAR(20) | | Contact phone for notification |
| party_size | INTEGER | NOT NULL | Number of guests |
| quoted_wait_minutes | INTEGER | | Estimated wait time |
| check_in_time | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | When added to waitlist |
| notified_at | TIMESTAMPTZ | | When notification sent |
| seated_at | TIMESTAMPTZ | | When seated |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'waiting' | waiting, notified, seated, left, removed |
| notes | TEXT | | Special requests or preferences |

---

## 9. Reporting Blueprint Tables

### 9.1 daily_summary

Pre-aggregated daily business metrics.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| business_date | DATE | NOT NULL, UNIQUE | Business date |
| gross_sales | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Total sales before discounts |
| net_sales | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Sales after discounts |
| tax_collected | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Total tax |
| discounts_given | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Total discounts |
| comps_given | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Total comps |
| refunds | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Total refunds |
| tips_collected | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Total tips |
| cash_sales | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Cash payments |
| credit_sales | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Credit/debit payments |
| other_sales | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Other payment types |
| order_count | INTEGER | NOT NULL, DEFAULT 0 | Number of orders |
| guest_count | INTEGER | NOT NULL, DEFAULT 0 | Number of guests |
| labor_hours | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | Total labor hours |
| labor_cost | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Total labor cost |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Report generation time |

### 9.2 hourly_sales

Hourly sales breakdown for trend analysis.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| business_date | DATE | NOT NULL | Business date |
| hour | INTEGER | NOT NULL | Hour (0-23) |
| sales_amount | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Sales in this hour |
| order_count | INTEGER | NOT NULL, DEFAULT 0 | Orders in this hour |
| guest_count | INTEGER | NOT NULL, DEFAULT 0 | Guests in this hour |

### 9.3 saved_report

User-saved report configurations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Report name |
| report_type | VARCHAR(50) | NOT NULL | Type of report |
| parameters | JSONB | NOT NULL, DEFAULT '{}' | Report parameters |
| *created_by_id* | INTEGER | FK, NOT NULL | User who created |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation time |
| is_scheduled | BOOLEAN | NOT NULL, DEFAULT FALSE | Auto-run on schedule |
| schedule_cron | VARCHAR(50) | | Cron expression for schedule |
| email_recipients | JSONB | DEFAULT '[]' | Email addresses for delivery |

### 9.4 report_execution

Log of report executions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *saved_report_id* | INTEGER | FK, NOT NULL | Report that was run |
| started_at | TIMESTAMPTZ | NOT NULL | Execution start |
| completed_at | TIMESTAMPTZ | | Execution end |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'running' | running, completed, failed |
| file_path | VARCHAR(500) | | Path to generated file |
| error_message | TEXT | | Error if failed |

### 9.5 audit_log

System-wide audit trail for sensitive actions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *user_id* | INTEGER | FK, NOT NULL | User who performed action |
| action | VARCHAR(50) | NOT NULL | Action type (e.g., 'void_order') |
| entity_type | VARCHAR(50) | NOT NULL | Entity type affected |
| entity_id | INTEGER | NOT NULL | Entity ID affected |
| old_values | JSONB | | Previous values |
| new_values | JSONB | | New values |
| ip_address | VARCHAR(45) | | Client IP address |
| user_agent | TEXT | | Client user agent |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | When action occurred |

---

## 10. Inventory Blueprint Tables

### 10.1 inventory_item

Inventory items (ingredients, supplies).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(150) | NOT NULL | Item name |
| sku | VARCHAR(50) | UNIQUE | SKU code |
| category | VARCHAR(30) | NOT NULL | protein, produce, dairy, dry_goods, beverage, paper, chemical, other |
| unit_of_measure | VARCHAR(20) | NOT NULL | Primary unit (lb, oz, each, case) |
| unit_cost | DECIMAL(10,4) | NOT NULL, DEFAULT 0 | Cost per unit |
| par_level | DECIMAL(10,2) | | Target stock level |
| reorder_point | DECIMAL(10,2) | | When to reorder |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Currently tracked |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update |

### 10.2 stock_level

Current stock quantities by location.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *inventory_item_id* | INTEGER | FK, NOT NULL | Inventory item |
| storage_location | VARCHAR(50) | NOT NULL, DEFAULT 'main' | Storage location name |
| quantity_on_hand | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | Current quantity |
| last_counted_at | TIMESTAMPTZ | | Last physical count |
| last_updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update |

### 10.3 recipe

Recipes linking menu items to inventory.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *menu_item_id* | INTEGER | FK, NOT NULL | Menu item this recipe makes |
| yield_quantity | DECIMAL(10,2) | NOT NULL, DEFAULT 1 | How many servings |
| yield_unit | VARCHAR(20) | NOT NULL, DEFAULT 'serving' | Unit of yield |
| instructions | TEXT | | Preparation instructions |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Recipe in use |

### 10.4 recipe_ingredient

Ingredients in a recipe.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *recipe_id* | INTEGER | FK, NOT NULL | Parent recipe |
| *inventory_item_id* | INTEGER | FK, NOT NULL | Ingredient |
| quantity | DECIMAL(10,4) | NOT NULL | Amount needed |
| unit | VARCHAR(20) | NOT NULL | Unit of measure |
| waste_factor_percent | DECIMAL(5,2) | DEFAULT 0 | Expected waste % |

### 10.5 vendor

Supplier/vendor information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(150) | NOT NULL | Vendor name |
| contact_name | VARCHAR(100) | | Primary contact |
| email | VARCHAR(255) | | Contact email |
| phone | VARCHAR(20) | | Contact phone |
| address | TEXT | | Business address |
| payment_terms | VARCHAR(50) | | Payment terms (e.g., Net 30) |
| lead_time_days | INTEGER | | Typical delivery lead time |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Active vendor |
| notes | TEXT | | Vendor notes |

### 10.6 purchase_order

Purchase orders to vendors.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| po_number | VARCHAR(20) | NOT NULL, UNIQUE | PO number |
| *vendor_id* | INTEGER | FK, NOT NULL | Vendor |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'draft' | draft, submitted, confirmed, partial, received, cancelled |
| order_date | DATE | | Date PO was placed |
| expected_date | DATE | | Expected delivery date |
| received_date | DATE | | Actual receive date |
| subtotal | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Pre-tax total |
| tax | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Tax amount |
| total | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Total amount |
| notes | TEXT | | PO notes |
| *created_by_id* | INTEGER | FK, NOT NULL | User who created |
| *approved_by_id* | INTEGER | FK, NULL | Manager who approved |

### 10.7 po_line_item

Line items on purchase orders.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *purchase_order_id* | INTEGER | FK, NOT NULL | Parent PO |
| *inventory_item_id* | INTEGER | FK, NOT NULL | Item being ordered |
| quantity_ordered | DECIMAL(10,2) | NOT NULL | Quantity ordered |
| unit_cost | DECIMAL(10,4) | NOT NULL | Cost per unit |
| quantity_received | DECIMAL(10,2) | DEFAULT 0 | Quantity received so far |
| received_at | TIMESTAMPTZ | | When received |

### 10.8 stock_adjustment

Manual stock adjustments (counts, waste, etc.).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *inventory_item_id* | INTEGER | FK, NOT NULL | Item adjusted |
| adjustment_type | VARCHAR(20) | NOT NULL | count, waste, theft, transfer, received, sold |
| quantity_change | DECIMAL(10,2) | NOT NULL | Amount changed (+/-) |
| reason | TEXT | | Reason for adjustment |
| *performed_by_id* | INTEGER | FK, NOT NULL | User who adjusted |
| *approved_by_id* | INTEGER | FK, NULL | Manager approval (if required) |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Adjustment time |

---

## 11. Customers Blueprint Tables

### 11.1 customer

Customer profiles for loyalty and CRM.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| first_name | VARCHAR(50) | | First name |
| last_name | VARCHAR(50) | | Last name |
| email | VARCHAR(255) | UNIQUE | Email address |
| phone | VARCHAR(20) | | Phone number |
| is_email_verified | BOOLEAN | NOT NULL, DEFAULT FALSE | Email confirmed |
| is_phone_verified | BOOLEAN | NOT NULL, DEFAULT FALSE | Phone confirmed |
| marketing_opt_in | BOOLEAN | NOT NULL, DEFAULT FALSE | Allows marketing |
| birthday | DATE | | Birthday for offers |
| anniversary | DATE | | Anniversary date |
| notes | TEXT | | Staff notes |
| tags | JSONB | DEFAULT '[]' | Customer tags |
| source | VARCHAR(20) | NOT NULL, DEFAULT 'pos' | pos, web, reservation, import |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Profile creation |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update |

### 11.2 loyalty_account

Customer loyalty program accounts.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *customer_id* | INTEGER | FK, NOT NULL, UNIQUE | Customer |
| *tier_id* | INTEGER | FK, NOT NULL | Current tier |
| points_balance | INTEGER | NOT NULL, DEFAULT 0 | Current points |
| lifetime_points | INTEGER | NOT NULL, DEFAULT 0 | Total points earned |
| points_expiring | INTEGER | DEFAULT 0 | Points expiring soon |
| expiration_date | DATE | | When points expire |
| enrolled_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Enrollment date |

### 11.3 loyalty_tier

Loyalty program tiers.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(50) | NOT NULL | Tier name (Bronze, Silver, Gold) |
| min_points | INTEGER | NOT NULL | Points needed for tier |
| multiplier | DECIMAL(3,2) | NOT NULL, DEFAULT 1.00 | Points earning multiplier |
| benefits | JSONB | DEFAULT '[]' | Tier benefits |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Tier is active |

### 11.4 gift_card

Gift card records.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| card_number | VARCHAR(20) | NOT NULL, UNIQUE | Card number |
| pin_hash | VARCHAR(255) | | Hashed PIN (if required) |
| initial_balance | DECIMAL(10,2) | NOT NULL | Starting balance |
| current_balance | DECIMAL(10,2) | NOT NULL | Current balance |
| *customer_id* | INTEGER | FK, NULL | Owner (if registered) |
| *purchased_by_id* | INTEGER | FK, NULL | Customer who purchased |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'active' | active, depleted, suspended, expired |
| issued_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Issue date |
| expires_at | DATE | | Expiration date |

### 11.5 feedback

Customer feedback and ratings.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *customer_id* | INTEGER | FK, NULL | Customer (if known) |
| *order_id* | INTEGER | FK, NULL | Related order |
| rating | INTEGER | NOT NULL | Overall rating (1-5) |
| food_rating | INTEGER | | Food rating (1-5) |
| service_rating | INTEGER | | Service rating (1-5) |
| ambiance_rating | INTEGER | | Ambiance rating (1-5) |
| comment | TEXT | | Customer comments |
| response | TEXT | | Management response |
| *responded_by_id* | INTEGER | FK, NULL | Who responded |
| responded_at | TIMESTAMPTZ | | Response time |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Feedback submission time |

---

## 12. Integrations Blueprint Tables

### 12.1 integration

Third-party integration configurations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Integration name |
| integration_type | VARCHAR(30) | NOT NULL | delivery, accounting, payroll, reservation, marketing, payment |
| provider | VARCHAR(50) | NOT NULL | Provider name (DoorDash, QuickBooks, etc.) |
| is_active | BOOLEAN | NOT NULL, DEFAULT FALSE | Integration enabled |
| config | JSONB | NOT NULL, DEFAULT '{}' | Configuration settings (encrypted) |
| credentials | JSONB | NOT NULL, DEFAULT '{}' | API credentials (encrypted) |
| last_sync_at | TIMESTAMPTZ | | Last successful sync |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Setup time |

### 12.2 webhook_endpoint

Outgoing webhook configurations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *integration_id* | INTEGER | FK, NOT NULL | Parent integration |
| url | VARCHAR(500) | NOT NULL | Webhook URL |
| secret_hash | VARCHAR(255) | | Signing secret |
| events | JSONB | NOT NULL, DEFAULT '[]' | Events to send |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Endpoint active |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation time |

### 12.3 external_order

Orders from third-party platforms.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *integration_id* | INTEGER | FK, NOT NULL | Source integration |
| external_id | VARCHAR(100) | NOT NULL | ID in external system |
| *order_id* | INTEGER | FK, NULL | Linked POS order |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'received' | received, accepted, rejected, preparing, ready, picked_up, delivered, cancelled |
| external_status | VARCHAR(50) | | Status in external system |
| raw_data | JSONB | NOT NULL | Original order data |
| received_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | When received |
| synced_at | TIMESTAMPTZ | | Last sync time |

### 12.4 sync_log

Integration sync history.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| **id** | SERIAL | PK | Unique identifier |
| *integration_id* | INTEGER | FK, NOT NULL | Integration |
| sync_type | VARCHAR(50) | NOT NULL | Type of sync operation |
| direction | VARCHAR(10) | NOT NULL | inbound, outbound |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'started' | started, completed, failed |
| records_processed | INTEGER | DEFAULT 0 | Number of records |
| errors | JSONB | DEFAULT '[]' | Error details |
| started_at | TIMESTAMPTZ | NOT NULL | Sync start time |
| completed_at | TIMESTAMPTZ | | Sync end time |

---

## 13. Recommended Indexes

Beyond primary keys and foreign keys (which should be indexed automatically), the following additional indexes are recommended for query performance:

### 13.1 Orders & Payments

| Index | Purpose |
|-------|---------|
| `order.status` | Filter open orders |
| `order.created_at` | Date range queries |
| `order.server_id, status` | Server's open orders |
| `order_item.order_id, status` | Items by order and status |
| `payment.created_at` | Payment date queries |
| `check.order_id` | Checks for an order |

### 13.2 Kitchen & Tables

| Index | Purpose |
|-------|---------|
| `kitchen_ticket.station_id, status` | Station's pending tickets |
| `kitchen_ticket.created_at` | Ticket timing queries |
| `table_status.status` | Find available tables |
| `reservation.reservation_time` | Reservations by date/time |
| `reservation.status` | Active reservations |

### 13.3 Reporting & Analytics

| Index | Purpose |
|-------|---------|
| `daily_summary.business_date` | Date lookups |
| `hourly_sales.business_date, hour` | Hourly breakdown queries |
| `audit_log.created_at` | Audit trail queries |
| `audit_log.user_id, created_at` | User activity lookup |

### 13.4 Staff & Time

| Index | Purpose |
|-------|---------|
| `user.email` | Login by email |
| `user.employee_number` | Lookup by employee ID |
| `time_entry.user_id, clock_in` | Employee time records |
| `shift.user_id, scheduled_start` | Employee schedules |

---

*--- End of Document ---*
