# CLAUDE.md - Restaurant POS System

Flask-based Restaurant POS using factory pattern and blueprint architecture.

## Tech Stack

Flask, PostgreSQL, SQLAlchemy, Flask-Login, Marshmallow, Jinja2, Materialize CSS 2.2.2, Vanilla JS (ES2022+), Google Material Symbols Rounded.

## Quick Reference

```bash
flask run                          # Dev server
flask db migrate -m "msg"          # Generate migration
flask db upgrade                   # Apply migrations
pytest                             # Run tests
pytest --cov=app                   # With coverage
```

## Architecture

- **12 Blueprints**: auth, api, menu, orders, payments, staff, kitchen, tables, reporting, inventory, customers, integrations
- **Blueprint structure**: `__init__.py`, `routes.py`, `models.py`, `services.py`, `schemas.py`, `forms.py`, `static/`, `templates/`
- **Service layer**: Routes delegate to services for business logic - keep routes thin
- **String FK references**: Use `db.ForeignKey('table.id')` to avoid circular imports

## Development Rules

### Code Conventions
1. Use service layer for business logic, keep routes thin
2. Use Marshmallow schemas for API serialization/validation
3. Blueprint assets in `blueprints/{name}/static/`, templates in `blueprints/{name}/templates/{name}/`
4. Tests in `tests/unit/test_{blueprint}/`

### Frontend Conventions
- **CSS**: Use `--pos-*` custom properties only (never hardcode colors/spacing)
- **CSS classes**: BEM-like with `pos-` prefix (`.pos-component-element--modifier`)
- **Icons**: `<span class="material-symbols-rounded" aria-hidden="true">icon_name</span>`
- **JS**: ES2022+ modules, event delegation, `const`/`let` only, strict equality
- **Touch**: Min 48x48px targets, use pointer events, 8px gap between targets
- **A11y**: WCAG 2.1 AA, 4.5:1 contrast, visible focus rings, proper ARIA labels

### HTML Requirements
- Semantic elements (`<nav>`, `<main>`, `<aside>`)
- `type="button"` on non-submit buttons
- Theme via `data-theme` attribute on `<html>`

## Jinja2 Macro Documentation

```jinja
{# macro_name(param1, param2=default)
   ----------------------------------
   Brief description.

   Parameters:
       param1 (type): Required. Description.
       param2 (type): Optional. Defaults to "value".
#}
```

## Documentation

- **UI/UX & Design System**: `docs/uiux.md`
- **Database schema**: `docs/database-schema.md`
- **API spec**: `docs/api-spec.yaml`
- **Architecture**: `docs/architecture.md`
- **Setup**: `docs/guides/installation.md`, `.env.example`
