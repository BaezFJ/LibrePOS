# Blueprint Architecture

> Detailed blueprint organization, tiers, ownership, and component responsibilities.

---

## Blueprint Overview by Tier

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

---

## Model Ownership

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

---

## Component Responsibilities

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
