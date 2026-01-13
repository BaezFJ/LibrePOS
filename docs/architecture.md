# LibrePOS System Architecture

> **Pattern:** Flask Blueprints with Factory Pattern
> **Blueprints:** 12 (10 Feature + 2 Supporting)
> **Database:** PostgreSQL
> **Version:** 1.0 | January 2026

---

## Design Principles

| Principle | Description |
|-----------|-------------|
| **Modular Blueprints** | Self-contained components with clear boundaries |
| **Factory Pattern** | Flexible configuration via `create_app()` |
| **Service Layer** | Routes → Services → Models (keep routes thin) |
| **Single Database** | PostgreSQL with cross-blueprint model imports |
| **Separated Auth** | Web (session) vs API (JWT-ready) authentication |

---

## Project Structure

```
librepos/
├── app/                          # Application package
│   ├── __init__.py               # Application factory (create_app)
│   ├── config.py                 # Configuration classes
│   ├── extensions.py             # Flask extension instances
│   ├── blueprints/               # 12 feature blueprints
│   ├── shared/                   # Decorators, helpers, validators
│   ├── static/                   # Global assets (vendor/, css/, js/)
│   └── templates/                # Base templates, layouts, macros
│
├── migrations/                   # Flask-Migrate (Alembic)
├── tests/                        # Unit, integration, e2e tests
├── docs/                         # Documentation
└── scripts/                      # Utility scripts
```

---

## Blueprint Overview

| Tier | Blueprint | Purpose |
|------|-----------|---------|
| **Support** | `auth` | Authentication, sessions, API keys |
| **Support** | `api` | RESTful API v1, OpenAPI docs |
| **Tier 1** | `menu` | Items, categories, modifiers, pricing |
| **Tier 1** | `orders` | Order lifecycle, items, checks |
| **Tier 1** | `payments` | Transactions, tips, discounts |
| **Tier 2** | `staff` | Users, roles, permissions, time tracking |
| **Tier 2** | `kitchen` | KDS, tickets, stations, routing |
| **Tier 2** | `tables` | Floor plans, reservations, waitlist |
| **Tier 3** | `reporting` | Sales, labor, analytics, audit logs |
| **Tier 3** | `inventory` | Stock, recipes, vendors, POs |
| **Tier 4** | `customers` | Profiles, loyalty, gift cards |
| **Tier 4** | `integrations` | Third-party, webhooks, external orders |

### Blueprint Structure

Each blueprint follows this standard layout:

```
app/blueprints/{name}/
├── __init__.py      # Blueprint registration
├── routes.py        # HTTP handlers
├── models.py        # SQLAlchemy models
├── services.py      # Business logic
├── schemas.py       # Marshmallow serializers
├── forms.py         # WTForms definitions
├── static/          # Blueprint CSS/JS
└── templates/{name}/# Blueprint templates
```

---

## URL Prefixes

| Blueprint | Web | API |
|-----------|-----|-----|
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

## Quick Reference

### Create Blueprint

```bash
mkdir -p app/blueprints/newfeature/{static/{css,js},templates/newfeature}
touch app/blueprints/newfeature/{__init__,routes,models,services,schemas,forms}.py
```

Register in `app/__init__.py`:
```python
from app.blueprints.newfeature import bp as newfeature_bp
app.register_blueprint(newfeature_bp, url_prefix='/newfeature')
```

### Add Model

```python
# blueprints/{name}/models.py
class NewModel(db.Model):
    __tablename__ = 'new_model'
    id = db.Column(db.Integer, primary_key=True)
```

```bash
flask db migrate -m "Add NewModel"
flask db upgrade
```

### Add Route

```python
# blueprints/{name}/routes.py
@bp.route('/new-page')
@login_required
def new_page():
    return render_template('blueprint/new_page.html')
```

---

## Architectural Decisions

| Area | Choice | Rationale |
|------|--------|-----------|
| Framework | Flask + factory pattern | Flexibility, modularity, testing |
| API | Separate versioned blueprint | Clean evolution (`/api/v1/...`) |
| Auth | Flask-Login (web), JWT-ready (API) | Simple + future mobile support |
| Frontend | MaterializeCSS + Chart.js + interact.js | Touch-friendly, modern |
| Testing | Pytest with fixtures | Powerful, readable |

---

## Detailed Documentation

**Architecture details:**
- [Blueprints](architecture/blueprints.md) - Tiers, ownership, routing
- [Templates](architecture/templates.md) - Layouts, macros, Jinja2 config
- [Static Assets](architecture/static-assets.md) - Asset organization, libraries
- [Configuration](architecture/configuration.md) - Environment, config classes
- [Database](architecture/database.md) - Migrations, cross-blueprint imports
- [Testing](architecture/testing.md) - Test structure, running tests

**Other documentation:**
- [UI/UX & Design System](uiux.md)
- [Database Schema](database-schema.md)
- [API Specification](api.md)
- [Installation Guide](guides/installation.md)
