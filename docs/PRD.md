# Restaurant Point of Sale System
## Product Requirements Document

**Version 1.0 | January 2026**

> **CONFIDENTIAL**

| Property | Value |
|----------|-------|
| Document Status | Draft - Pending Approval |
| Architecture Pattern | Flask Blueprints with Factory Pattern |
| Total Blueprints | 12 (10 Feature + 2 Supporting) |
| Database | Single PostgreSQL Database |

---

## 1. Executive Summary

This Product Requirements Document defines the technical architecture and implementation specifications for a comprehensive Restaurant Point of Sale (POS) system. The system is designed using Flask's blueprint architecture with a factory pattern, enabling modular development and phased deployment across four priority tiers.

The architecture supports both web-based interfaces using Jinja2 templating and a versioned RESTful API for future mobile and third-party integrations. Authentication is handled via Flask-Login for web sessions with a JWT-ready architecture for API authentication.

---

## 2. Scope

### 2.1 In Scope

The POS system encompasses the following functional domains organized by implementation priority:

**Tier 1: Core Foundation**
- **Menu Management:** Item configuration, categories, modifiers, pricing controls, combos, and scheduling
- **Order Management:** Order entry, types, lifecycle, modifications, check handling, and course management
- **Payment Processing:** Tender types, transactions, tips, adjustments, discounts, taxes, and receipts

**Tier 2: Operational Necessities**
- **Staff Management:** User accounts, roles and permissions, authentication, time tracking, scheduling, and tips
- **Kitchen Operations:** Ticket routing, KDS, order prioritization, course timing, and prep management
- **Table and Floor Management:** Floor plans, table configuration, status tracking, sections, reservations, and waitlist

**Tier 3: Business Optimization**
- **Reporting and Analytics:** Sales reports, product performance, labor reports, financial summaries, and dashboards
- **Inventory and Purchasing:** Stock tracking, recipes, purchase orders, receiving, vendors, and cost analysis

**Tier 4: Growth and Expansion**
- **Customer Management:** Profiles, loyalty programs, rewards, gift cards, feedback, and segmentation
- **Integrations and Channels:** Third-party delivery, online ordering, accounting, payroll, and API access

### 2.2 Out of Scope

Hardware procurement and installation, payment processor contracts, multi-tenancy support, and native mobile applications are not included in this initial release.

---

## 3. Architecture Overview

### 3.1 Design Principles

The system follows these core architectural principles:
- Modular blueprint structure with self-contained components
- Factory pattern for flexible application configuration
- Single database with cross-blueprint model imports
- Separation of web and API authentication concerns
- Layered service architecture within each blueprint

### 3.2 Blueprint Structure

Each blueprint is self-contained with its own models, routes, services, schemas, forms, static files, and templates. This structure enables independent development and testing while maintaining clear boundaries between functional domains.

**Blueprint Directory Structure:**

| Component | Purpose |
|-----------|---------|
| `__init__.py` | Blueprint registration and initialization |
| `routes.py` | HTTP route handlers and view functions |
| `models.py` | SQLAlchemy model definitions |
| `services.py` | Business logic and data operations |
| `schemas.py` | Marshmallow serialization schemas |
| `forms.py` | WTForms form definitions |
| `static/` | Blueprint-specific CSS, JavaScript, images |
| `templates/` | Jinja2 templates for blueprint views |

### 3.3 URL Structure

| Blueprint | Web Prefix | API Prefix |
|-----------|------------|------------|
| auth | `/auth` | `/api/v1/auth` |
| menu | `/menu` | `/api/v1/menu` |
| orders | `/orders` | `/api/v1/orders` |
| payments | `/payments` | `/api/v1/payments` |
| staff | `/staff` | `/api/v1/staff` |
| kitchen | `/kitchen` | `/api/v1/kitchen` |
| tables | `/tables` | `/api/v1/tables` |
| reporting | `/reports` | `/api/v1/reports` |
| inventory | `/inventory` | `/api/v1/inventory` |
| customers | `/customers` | `/api/v1/customers` |
| integrations | `/integrations` | `/api/v1/integrations` |

---

## 4. Technology Stack

### 4.1 Core Framework
- **Flask:** Web framework with blueprint support
- **Flask-SQLAlchemy:** ORM integration
- **Flask-Migrate:** Database migration management via Alembic
- **Flask-Login:** Session-based authentication
- **Flask-WTF:** Form handling and CSRF protection
- **python-dotenv:** Environment variable management

### 4.2 API and Serialization
- **marshmallow:** Object serialization and validation
- **flask-marshmallow:** Flask integration for marshmallow
- **marshmallow-sqlalchemy:** SQLAlchemy model serialization

### 4.3 Security
- **Flask-Bcrypt:** Password hashing
- **PyJWT:** JSON Web Token support for future API authentication

### 4.4 Database
- **PostgreSQL:** Primary database (psycopg2-binary driver)
- **SQLAlchemy:** ORM and database abstraction

### 4.5 Utilities
- **python-dateutil:** Advanced date and time handling
- **click:** CLI framework (included with Flask)

### 4.6 Development Dependencies
- **pytest** and **pytest-flask:** Testing framework
- **pytest-cov:** Code coverage reporting
- **factory-boy** and **faker:** Test data generation
- **black**, **flake8**, **isort:** Code formatting and linting

### 4.7 Frontend Styling and Interactivity
- **MaterializeCSS:** Modern responsive CSS framework based on Material Design
- **Chart.js:** Flexible JavaScript charting library for reports and dashboards
- **SortableJS:** Drag-and-drop reordering for lists and grids
- **interact.js:** Drag, resize, and gesture handling for floor plan editor

---

## 5. Frontend Framework Configuration

### 5.1 Overview

The frontend stack combines MaterializeCSS for consistent Material Design styling with specialized JavaScript libraries for interactive features. This approach provides a polished, professional appearance while enabling complex interactions required for POS operations such as drag-and-drop menu management and visual floor plan editing.

### 5.2 MaterializeCSS - Base Styling

MaterializeCSS serves as the base styling framework, providing Material Design components optimized for touch interfaces common in restaurant POS environments.

- Material Design components: cards, buttons, forms, modals, navigation
- Responsive grid system with 12-column layout
- Built-in JavaScript components: dropdowns, modals, tabs, toasts
- Touch-optimized interactions for mobile and tablet devices
- Color palette system with primary, secondary, and status colors
- Typography scale and spacing utilities

### 5.3 Chart.js - Data Visualization

Chart.js provides flexible, responsive charting capabilities for the reporting and analytics blueprint.

| Chart Type | Use Cases |
|------------|-----------|
| Line Charts | Sales trends over time, hourly sales patterns, year-over-year comparisons |
| Bar Charts | Sales by category, server performance comparisons, day-of-week analysis |
| Doughnut/Pie | Payment method distribution, product mix percentages, labor cost breakdown |
| Mixed Charts | Revenue vs covers overlay, sales vs labor cost correlation |

Chart.js configuration will include custom color schemes matching the MaterializeCSS theme, responsive sizing for dashboard widgets, and tooltip formatting for currency and percentage values.

### 5.4 SortableJS - Drag-and-Drop Reordering

SortableJS enables intuitive drag-and-drop reordering for list-based management interfaces throughout the application.

| Feature Area | Implementation |
|--------------|----------------|
| Menu Item Reordering | Drag items within categories to set display order, drag between categories to reassign |
| Category Management | Reorder menu categories, nest subcategories via drag-and-drop |
| Modifier Group Ordering | Set modifier group display sequence, reorder modifiers within groups |
| Course Sequencing | Drag order items between courses (appetizer, entree, dessert) |
| Station Assignment | Drag categories to kitchen stations for routing configuration |

SortableJS will be configured with animation effects, handle elements for precise control, and AJAX callbacks to persist order changes to the database.

### 5.5 interact.js - Floor Plan Editor

interact.js powers the visual floor plan editor in the tables blueprint, enabling restaurant managers to design and modify their floor layout with precision.

| Capability | Description |
|------------|-------------|
| Free Dragging | Position tables anywhere on the floor plan canvas with smooth movement |
| Snap to Grid | Optional grid snapping for aligned layouts (configurable grid size) |
| Table Resizing | Resize combined tables to represent merged seating arrangements |
| Rotation | Rotate tables to match physical orientation (45-degree increments) |
| Boundary Constraints | Keep tables within floor plan boundaries, prevent overlapping |
| Multi-Select | Select and move multiple tables simultaneously for section adjustments |

The floor plan editor will support multiple floors and rooms, with the ability to add fixed elements such as the bar, host stand, kitchen entrance, and restrooms as non-table obstacles.

### 5.6 File Structure

- `app/static/vendor/` - Third-party library files (MaterializeCSS, Chart.js, SortableJS, interact.js)
- `app/static/css/main.css` - Global custom styles extending MaterializeCSS
- `app/static/js/app.js` - Global JavaScript initialization and utilities
- Blueprint static folders - Feature-specific CSS and JavaScript modules

### 5.7 Theme Customization

MaterializeCSS will be customized via Sass variables to establish a consistent brand identity across the application. Custom theme tokens include primary and secondary brand colors, status indicator colors for orders and tables, and component sizing adjustments for touch-friendly tap targets (minimum 44px).

| Token Category | Purpose |
|----------------|---------|
| `$primary-color` | Brand primary for navigation, buttons, and interactive elements |
| `$secondary-color` | Accent color for highlights and secondary actions |
| `$success-color` | Positive status: completed orders, available tables, successful payments |
| `$error-color` | Alert status: voided items, payment failures, allergy warnings |
| `$warning-color` | Caution status: late tickets, low stock alerts, expiring items |
| `$info-color` | Informational: rush orders, VIP tables, special instructions |

### 5.8 Integration with Jinja2

MaterializeCSS classes are applied directly in Jinja2 templates. Common UI patterns are encapsulated in Jinja2 macros for reusability, including:
- Form field rendering with validation states
- Card components for menu items
- Status badges with appropriate colors
- Modal dialogs for confirmations

JavaScript initialization is handled via data attributes where possible, with custom initialization in blueprint-specific JavaScript files.

---

## 6. Template Engine Configuration

### 6.1 Jinja2 Extensions

- `jinja2.ext.do` - Execute statements within templates
- `jinja2.ext.loopcontrols` - Enable break and continue in loops
- `jinja2.ext.debug` - Debug output in development mode only

### 6.2 Custom Filters

- `currency` - Format monetary values with proper symbols and decimals
- `timeago` - Display relative timestamps
- `pluralize` - Smart pluralization for counts
- `status_badge` - Generate HTML badges for order and table statuses

### 6.3 Global Context Processors

- `current_location` - Active restaurant location for multi-location awareness
- `current_shift` - Active shift information for logged-in staff
- `permissions` - User permission set for conditional UI rendering

---

## 7. Authentication Strategy

### 7.1 Web Authentication (Flask-Login)

- Session-based authentication using Flask-Login
- PIN entry support for quick staff switching at terminals
- Configurable session timeout based on user role
- Manager override workflow for sensitive operations

### 7.2 API Authentication (JWT-Ready)

- Separate `@api_auth_required` decorator designed for JWT migration
- Token endpoint stubbed at `/api/v1/auth/token` for future implementation
- Refresh token support architecture planned
- API key authentication for third-party integrations

### 7.3 Model Organization

The User model resides in the staff blueprint as it contains employee data. Session management models (ActiveSession, LoginAttempt, APIKey) reside in the auth blueprint. Future RefreshToken model will be added to auth blueprint when JWT is implemented.

---

## 8. Data Models by Blueprint

Each blueprint contains its own models with cross-blueprint imports as needed. Models are imported at the top of model files to establish foreign key relationships. The following sections detail the primary models for each blueprint.

### 8.1 Auth Blueprint Models

| Model | Key Fields |
|-------|------------|
| LoginAttempt | id, user_id, attempt_time, success, ip_address, user_agent |
| ActiveSession | id, user_id, session_token, device_info, created_at, expires_at, is_active |
| APIKey | id, name, key_hash, user_id, scopes, created_at, expires_at, is_active, last_used_at |

### 8.2 Menu Blueprint Models

| Model | Key Fields |
|-------|------------|
| Category | id, name, description, display_order, parent_id, is_active, image_url |
| MenuItem | id, name, description, price, category_id, sku, is_available, is_taxable, prep_time_minutes |
| ModifierGroup | id, name, min_selections, max_selections, is_required, display_order |
| Modifier | id, name, price, modifier_group_id, is_available, display_order |
| Combo | id, name, description, price, is_active, start_date, end_date |
| PricingRule | id, menu_item_id, rule_type, price, start_time, end_time, days_of_week, priority |
| MenuSchedule | id, name, menu_items (M2M), start_date, end_date, days_of_week, start_time, end_time |

### 8.3 Orders Blueprint Models

| Model | Key Fields |
|-------|------------|
| Order | id, order_number, order_type, status, table_id, server_id, customer_id, guest_count, notes, created_at |
| OrderItem | id, order_id, menu_item_id, quantity, unit_price, notes, course, seat_number, status, void_reason |
| OrderItemModifier | id, order_item_id, modifier_id, quantity, unit_price |
| Check | id, order_id, check_number, subtotal, tax_amount, discount_amount, total, status, created_at |
| CheckItem | id, check_id, order_item_id |

### 8.4 Payments Blueprint Models

| Model | Key Fields |
|-------|------------|
| Payment | id, check_id, amount, tender_type, status, reference_number, processor_response, created_at |
| Tip | id, payment_id, amount, entry_method, declared_by_id, created_at, adjusted_at |
| Discount | id, name, discount_type, value, code, requires_authorization, is_active, usage_limit |
| TaxRate | id, name, rate, jurisdiction, applies_to, is_inclusive, is_active |
| CashDrawer | id, name, station_id, status, opened_at, opened_by_id, opening_amount, current_amount |
| Receipt | id, payment_id, receipt_type, delivery_method, content, delivered_at, email, phone |

### 8.5 Staff Blueprint Models

| Model | Key Fields |
|-------|------------|
| User | id, employee_number, first_name, last_name, email, phone, pin_hash, password_hash, role_id, is_active |
| Role | id, name, description, is_system_role, created_at |
| Permission | id, code, name, description, category |
| RolePermission | id, role_id, permission_id |
| TimeEntry | id, user_id, clock_in, clock_out, break_minutes, shift_id, is_edited, edit_reason |
| Shift | id, user_id, scheduled_start, scheduled_end, actual_start, actual_end, role_id, notes |
| TipDeclaration | id, user_id, shift_date, cash_tips, credit_tips, tip_out_given, tip_out_received |

### 8.6 Kitchen Blueprint Models

| Model | Key Fields |
|-------|------------|
| Station | id, name, station_type, display_order, is_active, printer_id |
| CategoryStation | id, category_id, station_id |
| KitchenTicket | id, order_id, station_id, status, priority, created_at, started_at, completed_at, bumped_at |
| KitchenTicketItem | id, ticket_id, order_item_id, quantity, notes, status, position |
| KitchenMessage | id, from_user_id, to_station_id, message, is_read, created_at |
| PrepTime | id, menu_item_id, station_id, average_seconds, sample_count, last_updated |

### 8.7 Tables Blueprint Models

| Model | Key Fields |
|-------|------------|
| FloorPlan | id, name, is_active, is_default, created_at |
| Table | id, floor_plan_id, table_number, name, capacity_min, capacity_max, x_position, y_position, shape |
| Section | id, floor_plan_id, name, color, created_at |
| TableStatus | id, table_id, status, party_size, server_id, order_id, seated_at, status_changed_at |
| Reservation | id, customer_name, phone, email, party_size, reservation_time, table_id, status, notes, source |
| WaitlistEntry | id, customer_name, phone, party_size, quoted_wait_minutes, check_in_time, status, notes |

### 8.8 Reporting Blueprint Models

| Model | Key Fields |
|-------|------------|
| DailySummary | id, business_date, gross_sales, net_sales, tax_collected, discounts_given, refunds, tips_collected |
| HourlySales | id, business_date, hour, sales_amount, order_count, guest_count |
| SavedReport | id, name, report_type, parameters, created_by_id, is_scheduled, schedule_cron, email_recipients |
| AuditLog | id, user_id, action, entity_type, entity_id, old_values, new_values, ip_address, created_at |

### 8.9 Inventory Blueprint Models

| Model | Key Fields |
|-------|------------|
| InventoryItem | id, name, sku, category, unit_of_measure, unit_cost, par_level, reorder_point, is_active |
| StockLevel | id, inventory_item_id, storage_location, quantity_on_hand, last_counted_at, last_updated_at |
| Recipe | id, menu_item_id, yield_quantity, yield_unit, instructions, is_active |
| RecipeIngredient | id, recipe_id, inventory_item_id, quantity, unit, waste_factor_percent |
| Vendor | id, name, contact_name, email, phone, address, payment_terms, lead_time_days, is_active |
| PurchaseOrder | id, po_number, vendor_id, status, order_date, expected_date, subtotal, tax, total, created_by_id |
| POLineItem | id, purchase_order_id, inventory_item_id, quantity_ordered, unit_cost, quantity_received |

### 8.10 Customers Blueprint Models

| Model | Key Fields |
|-------|------------|
| Customer | id, first_name, last_name, email, phone, marketing_opt_in, birthday, notes, tags, source |
| CustomerPreference | id, customer_id, preference_type, preference_value, notes |
| LoyaltyAccount | id, customer_id, tier_id, points_balance, lifetime_points, points_expiring, enrolled_at |
| LoyaltyTransaction | id, loyalty_account_id, transaction_type, points, order_id, description, created_at |
| Reward | id, name, description, points_required, reward_type, reward_value, menu_item_id, is_active |
| GiftCard | id, card_number, pin_hash, initial_balance, current_balance, status, issued_at, expires_at |
| Feedback | id, customer_id, order_id, rating, food_rating, service_rating, comment, response, created_at |

### 8.11 Integrations Blueprint Models

| Model | Key Fields |
|-------|------------|
| Integration | id, name, integration_type, provider, is_active, config, credentials, last_sync_at |
| WebhookEndpoint | id, integration_id, url, secret_hash, events, is_active, created_at |
| WebhookLog | id, endpoint_id, event_type, payload, response_status, response_body, sent_at, retry_count |
| ExternalOrder | id, integration_id, external_id, order_id, status, external_status, raw_data, received_at |
| SyncLog | id, integration_id, sync_type, direction, status, records_processed, errors, started_at |

---

## 9. CLI Commands

### 9.1 Application Commands (`flask pos`)

| Command | Description |
|---------|-------------|
| `flask pos init-db` | Create all database tables |
| `flask pos seed` | Seed database with sample development data |
| `flask pos seed --production` | Seed required data only (roles, permissions, tax rates) |
| `flask pos create-admin` | Interactive admin user creation wizard |
| `flask pos reset-db` | Drop all tables, recreate, and seed (development only) |

### 9.2 Testing Commands (`flask test`)

| Command | Description |
|---------|-------------|
| `flask test` | Run complete test suite |
| `flask test --coverage` | Run tests with coverage report generation |
| `flask test --blueprint menu` | Run tests for a specific blueprint only |
| `flask test --unit` | Run unit tests only |
| `flask test --integration` | Run integration tests only |

### 9.3 Database Commands (`flask db`)

| Command | Description |
|---------|-------------|
| `flask db migrate -m "msg"` | Generate new migration with message |
| `flask db upgrade` | Apply pending migrations |
| `flask db downgrade` | Rollback last migration |
| `flask db current` | Show current migration revision |
| `flask db history` | Show migration history |

### 9.4 Utility Commands (`flask util`)

| Command | Description |
|---------|-------------|
| `flask util routes` | List all registered routes with methods |
| `flask util permissions` | List all defined permissions by category |
| `flask util clear-sessions` | Clear expired sessions from database |
| `flask util export-schema` | Export OpenAPI schema for API documentation |

### 9.5 Report Commands (`flask report`)

| Command | Description |
|---------|-------------|
| `flask report daily --date YYYY-MM-DD` | Generate daily summary for specified date |
| `flask report eod` | Run end-of-day process and generate reports |

---

## 10. Seed Data Requirements

### 10.1 System Roles

The following roles are required for system operation and will be seeded during production deployment:

- **Admin:** Full system access
- **Manager:** Operational control and reporting
- **Server:** Order entry and table management
- **Bartender:** Bar orders and tab management
- **Cashier:** Payment processing
- **Host:** Reservations and seating
- **Kitchen:** Kitchen display access
- **Expo:** Expeditor view and coordination

### 10.2 Permissions by Category

**Orders**
- `create_order`, `modify_order`, `void_item`, `void_order`, `comp_item`, `transfer_check`

**Payments**
- `process_payment`, `apply_discount`, `process_refund`, `open_drawer`, `view_drawer`

**Menu**
- `view_menu`, `edit_menu`, `manage_pricing`, `manage_modifiers`

**Staff**
- `view_staff`, `manage_staff`, `edit_schedules`, `approve_timesheets`, `manage_roles`

**Reports**
- `view_basic_reports`, `view_financial_reports`, `export_reports`

**Kitchen**
- `view_kds`, `manage_stations`, `86_items`

**Tables**
- `manage_floor`, `manage_reservations`, `manage_waitlist`

**Inventory**
- `view_inventory`, `adjust_stock`, `create_po`, `receive_inventory`

**Customers**
- `view_customers`, `manage_loyalty`, `issue_gift_cards`

**Settings**
- `manage_integrations`, `manage_tax_rates`, `system_settings`

---

## 11. Implementation Phases

### Phase 1: Core Foundation (Tier 1)

Minimum viable POS functionality enabling basic restaurant operations.

| Blueprints | Deliverables |
|------------|--------------|
| auth | Login, logout, session management, PIN entry |
| menu | Item CRUD, categories, modifiers, pricing rules |
| orders | Order entry, modification, status tracking, check handling |
| payments | Payment processing, tips, discounts, receipts |

### Phase 2: Operational Readiness (Tier 2)

Features required for efficient daily restaurant operations.

| Blueprints | Deliverables |
|------------|--------------|
| staff | User management, roles, permissions, time tracking, scheduling |
| kitchen | KDS interface, ticket routing, station management, prep times |
| tables | Floor plan editor, table management, reservations, waitlist |

### Phase 3: Business Insights (Tier 3)

Analytics and inventory management for business optimization.

| Blueprints | Deliverables |
|------------|--------------|
| reporting | Sales reports, labor reports, dashboards, audit logs, scheduled reports |
| inventory | Stock tracking, recipes, purchase orders, vendor management, cost analysis |

### Phase 4: Growth Features (Tier 4)

Customer engagement and third-party ecosystem integration.

| Blueprints | Deliverables |
|------------|--------------|
| customers | Customer profiles, loyalty program, rewards, gift cards, feedback |
| integrations | Third-party delivery, accounting sync, payroll export, webhooks |
| api | RESTful API v1, OpenAPI documentation, API key management |

---

## 12. Summary of Architectural Decisions

| Decision Area | Choice |
|---------------|--------|
| Framework | Flask with factory pattern |
| Blueprint Count | 12 (10 feature + 2 supporting) |
| Blueprint Structure | Self-contained with own `static/` and `templates/` |
| API Strategy | Separate versioned api blueprint (`/api/v1/...`) |
| Template Engine | Jinja2 with extensions |
| Web Authentication | Flask-Login (session-based) |
| API Authentication | JWT-ready architecture (session initially) |
| Model Organization | Blueprint-owned with cross-imports |
| Database | Single PostgreSQL database |
| CLI Tools | Flask CLI commands with click |
| Frontend Styling | MaterializeCSS with Chart.js, SortableJS, interact.js |
| Starter Models | Included with basic fields per blueprint |

---

## 13. Appendix

### A. Directory Structure Overview

The application follows a standard Flask project layout with blueprints organized under `app/blueprints/`. Each blueprint contains its own models, routes, services, schemas, forms, static assets, and templates. Shared utilities reside in `app/shared/`, and base templates in `app/templates/`. Migrations are managed via Flask-Migrate in the `migrations/` directory, and tests mirror the blueprint structure under `tests/`.

```
app/
├── __init__.py              # Application factory
├── config.py                # Configuration classes
├── blueprints/
│   ├── auth/
│   ├── menu/
│   ├── orders/
│   ├── payments/
│   ├── staff/
│   ├── kitchen/
│   ├── tables/
│   ├── reporting/
│   ├── inventory/
│   ├── customers/
│   └── integrations/
├── shared/                  # Shared utilities
├── static/                  # Global static files
└── templates/               # Base templates
migrations/                  # Alembic migrations
tests/                       # Test suite
```

### B. Environment Configuration

Configuration is managed through environment variables loaded via python-dotenv. A `.env.example` file documents all required variables. Configuration classes (`DevelopmentConfig`, `TestingConfig`, `ProductionConfig`) in `app/config.py` provide environment-specific settings.

> **Security Note:** Sensitive values such as `SECRET_KEY`, `DATABASE_URL`, and integration credentials must never be committed to version control.

### C. Cross-Blueprint Model Import Pattern

Models reference other blueprints via standard Python imports at the top of model files. Foreign keys use string references to table names to avoid circular import issues.

**Example:**
```python
from app.blueprints.staff.models import User

server_id = db.Column(db.Integer, db.ForeignKey('user.id'))
```

---

*End of Document*
