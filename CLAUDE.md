# CLAUDE.md - Restaurant POS System

> Project guide for AI-assisted development

## Project Overview

A full-featured Restaurant Point of Sale (POS) system built with Flask using the factory pattern and blueprint architecture. The system handles menu management, order processing, payments, kitchen operations, staff management, inventory, customer loyalty, and third-party integrations.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask (Python) with factory pattern |
| Database | PostgreSQL (single database) |
| ORM | SQLAlchemy with Flask-Migrate |
| Authentication | Flask-Login (sessions), JWT-ready for API |
| Forms | Flask-WTF |
| Serialization | Flask-Marshmallow |
| Frontend | Jinja2 templates, Bootstrap 5.3.8 |
| Icons | Google Material Symbols Rounded |
| JS (Frontend) | Vanilla JavaScript (ES2022+) |
| Charts | Chart.js |
| Drag & Drop | SortableJS, interact.js |
| Testing | Pytest |

## UI/UX Philosophy

| Principle | Description |
|-----------|-------------|
| Mobile & Touch First | Components designed for touch before mouse/keyboard |
| Restaurant-Optimized | UI patterns for fast-paced restaurant environments |
| Accessibility First | WCAG 2.1 AA compliance mandatory |
| Performance Obsessed | Sub-second interactions, instant feedback |

> Full UI/UX specifications: see `docs/uiux.md`

## Design System

### CSS Custom Properties
All colors, spacing, and typography use `--pos-*` CSS custom properties. Never hardcode values.

| Category | Prefix | Example |
|----------|--------|---------|
| Brand colors | `--pos-primary`, `--pos-secondary` | `--pos-primary: #2563eb` |
| Semantic | `--pos-success`, `--pos-danger` | `--pos-danger: #ef4444` |
| Surfaces | `--pos-bg-*`, `--pos-text-*` | `--pos-bg-primary`, `--pos-text-secondary` |
| Spacing | `--pos-space-*` | `--pos-space-4` (16px) |

### Icons
Use Google Material Symbols Rounded. Include via CDN:
```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap" rel="stylesheet">
```

Usage:
```html
<span class="material-symbols-rounded" aria-hidden="true">shopping_cart</span>
```

### Theme Support
Dual theme (light/dark) via `data-theme` attribute on `<html>`. Theme variables auto-switch.

> See `docs/uiux.md` for full color palette, typography scale, and spacing values.

## Touch & Accessibility

### Touch Targets
- **Minimum size**: 48x48px for all interactive elements
- **Spacing**: 8px minimum gap between touch targets
- Use `pointerdown`/`pointerup` events for cross-device compatibility

### Accessibility (WCAG 2.1 AA)

| Requirement | Implementation |
|-------------|----------------|
| Color contrast | 4.5:1 normal text, 3:1 large text |
| Focus indicators | Visible focus rings on all interactive elements |
| Keyboard nav | All functionality keyboard accessible |
| Screen readers | Proper ARIA labels, live regions for dynamic content |
| Reduced motion | Respect `prefers-reduced-motion` |

### CSS Class Prefixes

| Prefix | Purpose |
|--------|---------|
| `.pos-btn-*` | Button variants |
| `.pos-card-*` | Card components |
| `.pos-menu-*` | Menu-related |
| `.pos-cart-*` | Cart/order |
| `.pos-sr-*` | Screen reader utilities |

> See `docs/uiux.md` for ARIA patterns, focus management, and component HTML examples.

## Directory Structure

```
restaurant-pos/
├── app/                          # Application package
│   ├── __init__.py               # Application factory (create_app)
│   ├── config.py                 # Configuration classes
│   ├── extensions.py             # Flask extension instances
│   ├── blueprints/               # Feature blueprints (12 total)
│   ├── shared/                   # Decorators, helpers, validators, exceptions
│   ├── static/                   # Global static assets (vendor/, css/, js/, img/)
│   └── templates/                # Base templates, layouts, macros, errors
├── migrations/                   # Flask-Migrate database migrations
├── tests/                        # Test suite (unit/, integration/, e2e/)
├── docs/                         # API and user documentation
├── scripts/                      # Utility scripts (seed_data.py, deploy.sh)
├── requirements.txt              # Python dependencies
└── requirements-dev.txt          # Development dependencies
```

## Blueprint Architecture

### All Blueprints (12 total)

| Blueprint | URL Prefix | Purpose |
|-----------|------------|---------|
| `auth` | `/auth` | Authentication, sessions, API keys |
| `api` | `/api/v1` | RESTful API endpoints |
| `menu` | `/menu` | Items, categories, modifiers, pricing |
| `orders` | `/orders` | Order lifecycle, items, checks |
| `payments` | `/payments` | Transactions, tips, discounts |
| `staff` | `/staff` | Users, roles, permissions, time tracking |
| `kitchen` | `/kitchen` | KDS, tickets, stations, routing |
| `tables` | `/tables` | Floor plans, reservations, waitlist |
| `reporting` | `/reporting` | Sales, labor, analytics, audit logs |
| `inventory` | `/inventory` | Stock, recipes, vendors, purchase orders |
| `customers` | `/customers` | Profiles, loyalty, gift cards |
| `integrations` | `/integrations` | Third-party, webhooks, external orders |

### Blueprint Internal Structure

Each blueprint follows this pattern:
```
app/blueprints/{blueprint_name}/
├── __init__.py       # Blueprint registration (bp = Blueprint(...))
├── routes.py         # HTTP route handlers (web + API)
├── models.py         # SQLAlchemy models
├── services.py       # Business logic layer
├── schemas.py        # Marshmallow serialization schemas
├── forms.py          # WTForms definitions
├── static/           # Blueprint-specific CSS/JS
└── templates/        # Blueprint-specific templates
```

## Key Patterns

### Application Factory
```python
# app/__init__.py
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # Initialize extensions
    # Register blueprints
    return app
```

### Cross-Blueprint Model Imports
```python
# Use string references for foreign keys to avoid circular imports
from app.blueprints.staff.models import User
from app.blueprints.menu.models import MenuItem

class Order(db.Model):
    server_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    server = db.relationship('User', backref='orders')
```

### Service Layer Pattern
Routes delegate to services for business logic:
```python
# routes.py
@bp.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    item = menu_service.create_item(data)
    return jsonify(item_schema.dump(item)), 201

# services.py
def create_item(data):
    item = MenuItem(**data)
    db.session.add(item)
    db.session.commit()
    return item
```

## Common Commands

```bash
# Run development server
flask run

# Database migrations
flask db init          # Initialize (first time only)
flask db migrate -m "description"  # Generate migration
flask db upgrade       # Apply migrations
flask db downgrade     # Rollback last migration

# Testing
pytest                           # Run all tests
pytest tests/unit/test_orders/   # Run specific tests
pytest --cov=app                 # Run with coverage

# Seed data
python scripts/seed_data.py
```

## Environment Variables

Required environment variables (see `.env.example`):
```
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost:5432/pos_dev
REDIS_URL=redis://localhost:6379/0
SESSION_TIMEOUT_MINUTES=480
JWT_SECRET_KEY=your-jwt-secret
PAYMENT_GATEWAY_API_KEY=pk_test_xxx
PAYMENT_GATEWAY_SECRET=sk_test_xxx
```

## Configuration Classes

- `Config` - Base configuration
- `DevelopmentConfig` - Debug enabled, local database
- `TestingConfig` - SQLite in-memory, testing flag
- `ProductionConfig` - Secure cookies, production database

## Template Layouts

- `base.html` - Master layout
- `layouts/admin.html` - Admin/back-office pages
- `layouts/pos.html` - POS terminal interface
- `layouts/kds.html` - Kitchen display system

## Creating New Features

### New Blueprint
```bash
mkdir -p app/blueprints/newfeature/{static/{css,js},templates/newfeature}
touch app/blueprints/newfeature/{__init__,routes,models,services,schemas,forms}.py
# Register in app/__init__.py
```

### New Model
```python
# 1. Define in models.py
class NewModel(db.Model):
    __tablename__ = 'new_model'
    id = db.Column(db.Integer, primary_key=True)

# 2. Generate and apply migration
flask db migrate -m "Add NewModel"
flask db upgrade
```

### New Route
```python
@bp.route('/new-page')
@login_required
def new_page():
    return render_template('blueprint/new_page.html')
```

## Development Guidelines

1. **Always use the service layer** for business logic - keep routes thin
2. **Use Marshmallow schemas** for API serialization and validation
3. **Reference foreign keys by string** (`db.ForeignKey('table.id')`) to avoid circular imports
4. **Blueprint-specific assets** go in `blueprints/{name}/static/`
5. **Template namespacing** - templates in `blueprints/{name}/templates/{name}/`
6. **Write tests** in the corresponding `tests/unit/test_{blueprint}/` directory
7. **HTML**: Use semantic elements (`<nav>`, `<main>`, `<aside>`), `type="button"` on non-submit buttons, proper `aria-*` attributes
8. **CSS**: BEM-like naming with `pos-` prefix (`.pos-component-element--modifier`), use CSS custom properties only
9. **JavaScript**: ES2022+ modules, event delegation, `const`/`let` only, strict equality
10. **Touch interactions**: Min 48x48px targets, use pointer events, provide immediate visual feedback

## Jinja2 Component Documentation Style

When documenting Jinja2 macro components, follow this format:

### File-Level Header
```jinja
{#
    Component Name
    ==============
    Brief description of the component and its purpose.

    Import:
        {% import "components/_example.html" as Example %}

    Basic Usage:
        {{ Example.macro_name("param") }}

    Advanced Usage:
        {% call Example.container() %}
            {{ Example.item("nested") }}
        {% endcall %}

    Context Variables:
        var_name - Description of context variable

    Note: Any important notes (e.g., JS initialization requirements).
#}
```

### Macro Documentation
```jinja
{# macro_name(param1, param2=default)
   ----------------------------------
   Brief description of what the macro does.

   Parameters:
       param1 (type): Required. Description of the parameter.
       param2 (type): Optional. Description. Defaults to "value".

   Usage: Additional usage notes for {% call %} macros.
#}
{% macro macro_name(param1, param2=default) %}
```

### Style Rules
- **Header underline**: Use `=` for component title, `-` for macro names (match length)
- **Parameter format**: `name (type): Required/Optional. Description.`
- **Types**: Use `str`, `bool`, `int`, or specific values
- **Examples**: Place in file header, not in individual macro docs
- **Call macros**: Add `Usage:` note explaining `{% call %}` requirement

## Related Documentation

- **UI/UX Guidelines: see docs/uiux.md** *(design system, components, accessibility)*
- Product requirements: see docs/PRD.md
- Database schema: see docs/database-schema.md
- Application structure: see docs/architecture.md
- API documentation: see docs/api.md
- API specification: see docs/api-spec.yaml
- UI components: see docs/components.md
- Feature roadmap: see docs/roadmap.md
- Installation guide: see docs/guides/installation.md
- Environment configuration: see docs/guides/environment.md
- Database configuration: see docs/guides/database.md