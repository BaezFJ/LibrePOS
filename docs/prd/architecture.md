# Architecture

> Design principles, blueprint structure, and URL organization

---

## Design Principles

The system follows these core architectural principles:

- Modular blueprint structure with self-contained components
- Factory pattern for flexible application configuration
- Single database with cross-blueprint model imports
- Separation of web and API authentication concerns
- Layered service architecture within each blueprint

---

## Blueprint Structure

Each blueprint is self-contained with its own models, routes, services, schemas, forms, static files, and templates. This structure enables independent development and testing while maintaining clear boundaries between functional domains.

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

---

## URL Structure

| Blueprint | Web Prefix | API Prefix |
|-----------|------------|------------|
| auth | `/auth` | `/api/v1/auth` |
| menu | `/menu` | `/api/v1/menu` |
| orders | `/orders` | `/api/v1/orders` |
| payments | `/payments` | `/api/v1/payments` |
| operations | `/operations` | `/api/v1/operations` |
| staff | `/staff` | `/api/v1/staff` |
| reporting | `/reports` | `/api/v1/reports` |

---

## Directory Structure

```
app/
├── __init__.py              # Application factory
├── config.py                # Configuration classes
├── blueprints/
│   ├── api/
│   ├── auth/
│   ├── menu/
│   ├── operations/
│   ├── orders/
│   ├── payments/
│   ├── reporting/
│   └── staff/
├── shared/                  # Shared utilities
├── static/                  # Global static files
└── templates/               # Base templates
migrations/                  # Alembic migrations
tests/                       # Test suite
```

---

## Cross-Blueprint Model Import Pattern

Models reference other blueprints via standard Python imports. Foreign keys use string references to table names to avoid circular import issues.

```python
from app.blueprints.staff.models import User

server_id = db.Column(db.Integer, db.ForeignKey('user.id'))
```

---

## Environment Configuration

Configuration is managed through environment variables loaded via python-dotenv. A `.env.example` file documents all required variables. Configuration classes (`DevelopmentConfig`, `TestingConfig`, `ProductionConfig`) in `app/config.py` provide environment-specific settings.

> **Security Note:** Sensitive values such as `SECRET_KEY`, `DATABASE_URL`, and integration credentials must never be committed to version control.
