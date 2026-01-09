# LibrePOS System – Application Structure

> **Architecture Pattern:** Flask Blueprints with Factory Pattern  
> **Total Blueprints:** 12 (10 Feature + 2 Supporting)  
> **Database:** Single PostgreSQL Database  
> **Version:** 1.0 | January 2026

---

## Table of Contents

1. [Design Principles](#design-principles)
2. [Project Root Structure](#project-root-structure)
3. [Application Directory Structure](#application-directory-structure)
4. [Blueprint Architecture](#blueprint-architecture)
5. [Blueprint Directory Structure](#blueprint-directory-structure)
6. [URL Routing Structure](#url-routing-structure)
7. [Static Assets Organization](#static-assets-organization)
8. [Template Organization](#template-organization)
9. [Configuration Management](#configuration-management)
10. [Database & Migrations](#database--migrations)
11. [Testing Structure](#testing-structure)
12. [Summary of Architectural Decisions](#summary-of-architectural-decisions)

---

## Design Principles

The system follows these core architectural principles:

| Principle | Description |
|-----------|-------------|
| **Modular Blueprint Structure** | Self-contained components with clear boundaries |
| **Factory Pattern** | Flexible application configuration via `create_app()` |
| **Single Database** | PostgreSQL with cross-blueprint model imports |
| **Separated Auth Concerns** | Web (session) vs API (JWT-ready) authentication |
| **Layered Service Architecture** | Routes → Services → Models within each blueprint |

---

## Project Root Structure

```
librepos/
├── app/                          # Application package
│   ├── __init__.py               # Application factory (create_app)
│   ├── config.py                 # Configuration classes
│   ├── extensions.py             # Flask extension instances
│   ├── blueprints/               # Feature blueprints (see below)
│   ├── shared/                   # Shared utilities and helpers
│   ├── static/                   # Global static assets
│   └── templates/                # Base templates and layouts
│
├── migrations/                   # Flask-Migrate database migrations
│   ├── versions/                 # Migration version files
│   ├── alembic.ini
│   ├── env.py
│   └── script.py.mako
│
├── tests/                        # Test suite (mirrors blueprint structure)
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   ├── unit/                     # Unit tests by blueprint
│   ├── integration/              # Integration tests
│   └── e2e/                      # End-to-end tests
│
├── docs/                         # Documentation
│   ├── api/                      # API documentation
│   └── guides/                   # User and developer guides
│
├── scripts/                      # Utility scripts
│   ├── seed_data.py              # Database seeding
│   └── deploy.sh                 # Deployment scripts
│
├── .env.example                  # Environment variable template
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── requirements-dev.txt          # Development dependencies
├── pyproject.toml                # Project metadata
├── Makefile                      # Common commands
└── README.md                     # Project documentation
```

---

## Application Directory Structure

```
app/
├── __init__.py                   # Application factory
│   └── create_app()              # Returns configured Flask app
│
├── config.py                     # Configuration classes
│   ├── Config                    # Base configuration
│   ├── DevelopmentConfig         # Development settings
│   ├── TestingConfig             # Test settings
│   └── ProductionConfig          # Production settings
│
├── extensions.py                 # Centralized extension instances
│   ├── db                        # SQLAlchemy
│   ├── migrate                   # Flask-Migrate
│   ├── login_manager             # Flask-Login
│   ├── marshmallow               # Flask-Marshmallow
│   └── csrf                      # Flask-WTF CSRF
│
├── blueprints/                   # All feature blueprints
│   ├── __init__.py               # Blueprint registration helper
│   ├── auth/                     # Authentication & sessions
│   ├── menu/                     # Menu management
│   ├── orders/                   # Order management
│   ├── payments/                 # Payment processing
│   ├── staff/                    # Staff management
│   ├── kitchen/                  # Kitchen operations
│   ├── tables/                   # Table & floor management
│   ├── reporting/                # Reports & analytics
│   ├── inventory/                # Inventory & purchasing
│   ├── customers/                # Customer management
│   ├── integrations/             # Third-party integrations
│   └── api/                      # RESTful API (v1)
│
├── shared/                       # Shared utilities
│   ├── __init__.py
│   ├── decorators.py             # Custom decorators
│   ├── helpers.py                # Helper functions
│   ├── validators.py             # Custom validators
│   └── exceptions.py             # Custom exceptions
│
├── static/                       # Global static assets
│   ├── vendor/                   # Third-party libraries
│   │   ├── materialize/          # MaterializeCSS
│   │   ├── chartjs/              # Chart.js
│   │   ├── sortablejs/           # SortableJS
│   │   └── interactjs/           # interact.js
│   ├── css/
│   │   └── main.css              # Global custom styles
│   ├── js/
│   │   └── app.js                # Global JavaScript
│   └── img/                      # Global images
│
└── templates/                    # Base templates
    ├── base.html                 # Master layout template
    ├── layouts/                  # Layout variations
    │   ├── admin.html            # Admin/back-office layout
    │   ├── pos.html              # POS terminal layout
    │   └── kds.html              # Kitchen display layout
    ├── macros/                   # Reusable Jinja2 macros
    │   ├── forms.html            # Form field macros
    │   ├── cards.html            # Card component macros
    │   ├── badges.html           # Status badge macros
    │   └── modals.html           # Modal dialog macros
    └── errors/                   # Error pages
        ├── 404.html
        ├── 403.html
        └── 500.html
```

---

## Blueprint Architecture

### Blueprint Overview by Tier

| Tier | Blueprint | Purpose | Dependencies |
|------|-----------|---------|--------------|
| **Supporting** | `auth` | Authentication, sessions, API keys | staff (User model) |
| **Supporting** | `api` | RESTful API v1, OpenAPI docs | All blueprints |
| **Tier 1** | `menu` | Items, categories, modifiers, pricing | - |
| **Tier 1** | `orders` | Order lifecycle, items, checks | menu, staff, tables |
| **Tier 1** | `payments` | Transactions, tips, discounts | orders, staff, customers |
| **Tier 2** | `staff` | Users, roles, permissions, time tracking | - |
| **Tier 2** | `kitchen` | KDS, tickets, stations, routing | orders, menu |
| **Tier 2** | `tables` | Floor plans, reservations, waitlist | staff |
| **Tier 3** | `reporting` | Sales, labor, analytics, audit logs | orders, payments, staff |
| **Tier 3** | `inventory` | Stock, recipes, vendors, POs | menu |
| **Tier 4** | `customers` | Profiles, loyalty, gift cards | orders, payments |
| **Tier 4** | `integrations` | Third-party, webhooks, external orders | orders, menu |

### Model Ownership

Each blueprint owns its models. Cross-blueprint relationships use imports:

```python
# Example: orders/models.py
from app.blueprints.staff.models import User
from app.blueprints.menu.models import MenuItem

class Order(db.Model):
    server_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Foreign keys use string table names to avoid circular imports
```

---

## Blueprint Directory Structure

Each blueprint is self-contained with this standardized structure:

```
app/blueprints/{blueprint_name}/
├── __init__.py                   # Blueprint registration
│   └── bp = Blueprint(...)       # Blueprint instance
│
├── routes.py                     # HTTP route handlers
│   ├── Web routes                # HTML page views
│   └── API routes                # JSON API endpoints
│
├── models.py                     # SQLAlchemy models
│   └── Model classes             # Database table definitions
│
├── services.py                   # Business logic layer
│   └── Service functions         # Data operations, validations
│
├── schemas.py                    # Marshmallow schemas
│   └── Serializers               # JSON serialization/validation
│
├── forms.py                      # WTForms definitions
│   └── Form classes              # Web form handling
│
├── static/                       # Blueprint-specific assets
│   ├── css/
│   │   └── {blueprint}.css       # Blueprint styles
│   └── js/
│       └── {blueprint}.js        # Blueprint JavaScript
│
└── templates/                    # Blueprint templates
    └── {blueprint}/              # Namespaced template folder
        ├── index.html
        ├── detail.html
        ├── create.html
        └── partials/             # Template fragments
            └── _list_item.html
```

### Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| `__init__.py` | Blueprint registration, initialization, imports |
| `routes.py` | HTTP handlers, request/response, view logic |
| `models.py` | Database schema, relationships, model methods |
| `services.py` | Business logic, data access, complex operations |
| `schemas.py` | API serialization, input validation |
| `forms.py` | Web form definitions, field validation |
| `static/` | Blueprint-specific CSS, JS, images |
| `templates/` | Jinja2 templates for blueprint views |

---

## URL Routing Structure

### Web Routes (Jinja2 Templates)

| Blueprint | URL Prefix | Example Routes |
|-----------|------------|----------------|
| `auth` | `/auth` | `/auth/login`, `/auth/logout`, `/auth/pin` |
| `menu` | `/menu` | `/menu/items`, `/menu/categories`, `/menu/modifiers` |
| `orders` | `/orders` | `/orders/new`, `/orders/<id>`, `/orders/<id>/items` |
| `payments` | `/payments` | `/payments/process`, `/payments/receipts/<id>` |
| `staff` | `/staff` | `/staff/users`, `/staff/roles`, `/staff/schedule` |
| `kitchen` | `/kitchen` | `/kitchen/kds`, `/kitchen/tickets`, `/kitchen/stations` |
| `tables` | `/tables` | `/tables/floor`, `/tables/reservations`, `/tables/waitlist` |
| `reporting` | `/reports` | `/reports/daily`, `/reports/sales`, `/reports/labor` |
| `inventory` | `/inventory` | `/inventory/items`, `/inventory/vendors`, `/inventory/orders` |
| `customers` | `/customers` | `/customers/profiles`, `/customers/loyalty`, `/customers/gift-cards` |
| `integrations` | `/integrations` | `/integrations/delivery`, `/integrations/webhooks` |

### API Routes (JSON Responses)

| Blueprint | API Prefix | Example Endpoints |
|-----------|------------|-------------------|
| `auth` | `/api/v1/auth` | `POST /login`, `POST /logout`, `GET /me` |
| `menu` | `/api/v1/menu` | `GET /items`, `POST /items`, `PATCH /items/<id>/availability` |
| `orders` | `/api/v1/orders` | `GET /`, `POST /`, `POST /<id>/submit` |
| `payments` | `/api/v1/payments` | `POST /process`, `POST /<id>/void`, `POST /<id>/refund` |
| `staff` | `/api/v1/staff` | `GET /users`, `POST /clock-in`, `POST /clock-out` |
| `kitchen` | `/api/v1/kitchen` | `GET /tickets`, `POST /tickets/<id>/bump` |
| `tables` | `/api/v1/tables` | `GET /`, `POST /<id>/seat`, `PATCH /<id>/status` |
| `reporting` | `/api/v1/reports` | `GET /daily-summary`, `GET /sales`, `GET /audit-log` |
| `inventory` | `/api/v1/inventory` | `GET /items`, `POST /items/<id>/adjust` |
| `customers` | `/api/v1/customers` | `GET /`, `GET /lookup`, `POST /loyalty/redeem` |
| `integrations` | `/api/v1/integrations` | `GET /`, `POST /<id>/sync`, `POST /webhooks` |

---

## Static Assets Organization

### Global Assets (`app/static/`)

```
app/static/
├── vendor/                       # Third-party libraries
│   ├── materialize/
│   │   ├── css/materialize.min.css
│   │   └── js/materialize.min.js
│   ├── chartjs/
│   │   └── chart.min.js
│   ├── sortablejs/
│   │   └── Sortable.min.js
│   └── interactjs/
│       └── interact.min.js
│
├── css/
│   ├── main.css                  # Global custom styles
│   ├── variables.css             # CSS custom properties (theme)
│   └── utilities.css             # Utility classes
│
├── js/
│   ├── app.js                    # Global initialization
│   ├── api.js                    # API client utilities
│   └── utils.js                  # Helper functions
│
└── img/
    ├── logo.svg                  # Application logo
    ├── icons/                    # Custom icons
    └── placeholders/             # Placeholder images
```

### Blueprint-Specific Assets

```
app/blueprints/kitchen/static/
├── css/
│   └── kds.css                   # KDS-specific styles
└── js/
    ├── kds.js                    # KDS functionality
    └── ticket-manager.js         # Ticket operations

app/blueprints/tables/static/
├── css/
│   └── floor-plan.css            # Floor plan editor styles
└── js/
    ├── floor-editor.js           # interact.js floor plan editor
    └── reservation-calendar.js   # Reservation management
```

### Frontend Libraries

| Library | Version | Purpose | Location |
|---------|---------|---------|----------|
| MaterializeCSS | 2.2.2   | UI framework, components | `vendor/materialize/` |
| Chart.js | 4.x     | Dashboard charts | `vendor/chartjs/` |
| SortableJS | 1.15.x  | Drag-drop reordering | `vendor/sortablejs/` |
| interact.js | 1.10.x  | Floor plan editor | `vendor/interactjs/` |

---

## Template Organization

### Base Templates (`app/templates/`)

```
app/templates/
├── base.html                     # Master template
│   ├── <!DOCTYPE html>
│   ├── <head> meta, CSS links
│   ├── {% block content %}
│   └── <scripts> JS includes
│
├── layouts/
│   ├── admin.html                # Back-office layout (sidebar nav)
│   ├── pos.html                  # POS terminal layout (full-screen)
│   └── kds.html                  # Kitchen display (no nav, auto-refresh)
│
├── macros/
│   ├── forms.html                # {{ form_field(field) }}
│   ├── cards.html                # {{ menu_item_card(item) }}
│   ├── badges.html               # {{ status_badge(status) }}
│   └── modals.html               # {{ confirm_modal(id, title) }}
│
├── components/
│   ├── _navbar.html              # Navigation bar partial
│   ├── _sidebar.html             # Admin sidebar partial
│   ├── _pagination.html          # Pagination controls
│   └── _flash_messages.html      # Alert messages
│
└── errors/
    ├── 404.html                  # Not found
    ├── 403.html                  # Forbidden
    └── 500.html                  # Server error
```

### Blueprint Templates

```
app/blueprints/orders/templates/orders/
├── index.html                    # Order list view
├── detail.html                   # Single order view
├── entry.html                    # Order entry screen
├── checkout.html                 # Payment/checkout screen
└── partials/
    ├── _order_item.html          # Order item row
    ├── _order_totals.html        # Order totals display
    └── _modifier_selector.html   # Modifier selection modal
```

### Jinja2 Configuration

**Extensions:**
- `jinja2.ext.do` - Execute statements in templates
- `jinja2.ext.loopcontrols` - Break/continue in loops
- `jinja2.ext.debug` - Debug output (development only)

**Custom Filters:**
| Filter | Purpose | Example |
|--------|---------|---------|
| `currency` | Format money | `{{ 12.50 \| currency }}` → `$12.50` |
| `timeago` | Relative time | `{{ created_at \| timeago }}` → `5 min ago` |
| `pluralize` | Smart plural | `{{ count \| pluralize('item') }}` |
| `status_badge` | Status HTML | `{{ 'completed' \| status_badge }}` |

**Context Processors:**
| Variable | Purpose |
|----------|---------|
| `current_location` | Active restaurant location |
| `current_shift` | Active shift for logged-in staff |
| `permissions` | User permission set for UI conditionals |

---

## Configuration Management

### Environment Variables (`.env`)

```bash
# Application
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/pos_dev

# Redis (sessions, caching)
REDIS_URL=redis://localhost:6379/0

# Authentication
SESSION_TIMEOUT_MINUTES=480
JWT_SECRET_KEY=your-jwt-secret

# Payment Gateway
PAYMENT_GATEWAY_API_KEY=pk_test_xxx
PAYMENT_GATEWAY_SECRET=sk_test_xxx

# Integrations
DOORDASH_API_KEY=xxx
UBEREATS_API_KEY=xxx
QUICKBOOKS_CLIENT_ID=xxx
```

### Configuration Classes (`app/config.py`)

```python
class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
class ProductionConfig(Config):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SESSION_COOKIE_SECURE = True
```

---

## Database & Migrations

### Migration Directory

```
migrations/
├── alembic.ini                   # Alembic configuration
├── env.py                        # Migration environment
├── script.py.mako                # Migration template
└── versions/                     # Migration files
    ├── 001_initial_schema.py
    ├── 002_add_inventory.py
    └── 003_add_loyalty.py
```

### Common Commands

```bash
# Initialize migrations (first time only)
flask db init

# Generate migration after model changes
flask db migrate -m "Add customer loyalty tables"

# Apply migrations
flask db upgrade

# Rollback last migration
flask db downgrade

# Show migration history
flask db history
```

### Cross-Blueprint Model Imports

```python
# Pattern for cross-blueprint foreign keys
# In: app/blueprints/orders/models.py

from app.blueprints.staff.models import User
from app.blueprints.menu.models import MenuItem

class Order(db.Model):
    __tablename__ = 'order'
    
    # Use string reference to avoid circular imports
    server_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationship with backref
    server = db.relationship('User', backref='orders')
```

---

## Testing Structure

```
tests/
├── __init__.py
├── conftest.py                   # Shared fixtures
│   ├── app fixture               # Test app instance
│   ├── client fixture            # Test client
│   ├── db fixture                # Test database
│   └── auth fixtures             # Logged-in user states
│
├── unit/                         # Unit tests (isolated)
│   ├── test_menu/
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_schemas.py
│   ├── test_orders/
│   ├── test_payments/
│   └── ...
│
├── integration/                  # Integration tests
│   ├── test_order_flow.py        # Order → Payment flow
│   ├── test_kitchen_routing.py   # Order → Kitchen tickets
│   └── test_inventory_deduct.py  # Sale → Stock adjustment
│
└── e2e/                          # End-to-end tests
    ├── test_complete_sale.py     # Full customer journey
    └── test_shift_workflow.py    # Clock in → Sales → Clock out
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific blueprint tests
pytest tests/unit/test_orders/

# Run with coverage
pytest --cov=app --cov-report=html

# Run integration tests only
pytest tests/integration/
```

---

## Summary of Architectural Decisions

| Decision Area | Choice | Rationale |
|---------------|--------|-----------|
| **Framework** | Flask with factory pattern | Flexibility, modularity, testing |
| **Blueprint Count** | 12 (10 feature + 2 supporting) | Clear domain separation |
| **Blueprint Structure** | Self-contained with own `static/` and `templates/` | Independent development |
| **API Strategy** | Separate versioned `api` blueprint (`/api/v1/...`) | Clean API evolution |
| **Template Engine** | Jinja2 with extensions | Powerful, familiar, integrated |
| **Web Authentication** | Flask-Login (session-based) | Simple, secure for web |
| **API Authentication** | JWT-ready architecture | Future mobile/integration support |
| **Model Organization** | Blueprint-owned with cross-imports | Clear ownership, relationships |
| **Database** | Single PostgreSQL database | Transactional integrity |
| **CLI Tools** | Flask CLI commands with Click | Consistent interface |
| **Frontend Styling** | MaterializeCSS + Chart.js + SortableJS + interact.js | Modern, touch-friendly |
| **Testing** | Pytest with fixtures | Powerful, readable tests |

---

## Quick Reference

### Creating a New Blueprint

```bash
# 1. Create blueprint directory
mkdir -p app/blueprints/newfeature/{static/{css,js},templates/newfeature}

# 2. Create required files
touch app/blueprints/newfeature/{__init__,routes,models,services,schemas,forms}.py

# 3. Register in app factory (app/__init__.py)
from app.blueprints.newfeature import bp as newfeature_bp
app.register_blueprint(newfeature_bp, url_prefix='/newfeature')
```

### Adding a New Model

```python
# 1. Define in blueprint's models.py
class NewModel(db.Model):
    __tablename__ = 'new_model'
    id = db.Column(db.Integer, primary_key=True)
    # ... fields

# 2. Generate migration
flask db migrate -m "Add NewModel"

# 3. Apply migration
flask db upgrade
```

### Adding a New Route

```python
# In blueprint's routes.py
@bp.route('/new-page')
@login_required
def new_page():
    return render_template('blueprint/new_page.html')

# For API endpoint
@bp.route('/api/v1/resource', methods=['POST'])
@api_auth_required
def create_resource():
    return jsonify({'success': True}), 201
```

---

*Document generated from POS System PRD v1.0*
