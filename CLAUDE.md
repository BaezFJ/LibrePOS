# LibrePOS - Restaurant POS System

Flask-based Restaurant POS using factory pattern and blueprint architecture.

## Tech Stack

Flask, PostgreSQL, SQLAlchemy, Flask-Login, Marshmallow, Jinja2, Materialize CSS 2.2.2, Vanilla JS (ES2022+), Google Material Symbols Rounded.

## Commands

```bash
flask run                    # Dev server
flask db migrate -m "msg"    # Generate migration
flask db upgrade             # Apply migrations
.venv/bin/pytest             # Run tests
.venv/bin/pytest --cov=app   # With coverage
npx clean-css-cli -o <out>.min.css <in>.css  # Minify CSS
```

## Architecture

- **8 Blueprints**: auth, api, menu, orders, payments, operations, staff, reporting
- **Blueprint structure**: `__init__.py`, `routes.py`, `models.py`, `services.py`, `schemas.py`, `forms.py`, `static/`, `templates/`

## Critical Rules

**IMPORTANT - You MUST follow these:**

1. **Service layer**: Routes delegate to services for business logic. NEVER put business logic in routes.
2. **String FK references**: Use `db.ForeignKey('table.id')` to avoid circular imports.
3. **CSS variables**: Use `var(--md-sys-color-*)` for theming, `var(--pos-*)` for spacing/typography. Theme: elegant restaurant palette (warm cream/espresso light, charcoal/amber dark).
4. **CSS strategy**: Materialize CSS first. Use `.pos-*` prefix ONLY for POS-specific components (terminal, cart).
5. **Utility classes**: Atomic/composable pattern (`.flex .flex-row .gap-4`). Responsive prefixes: `m:`, `l:`, `xl:` (Materialize breakpoints).
6. **CSS file organization**: `utilities.css` = atomic utilities only. `main.css` = components (BEM classes, element selectors). `override.css` = Materialize overrides. `variables.css` = custom properties.
7. **Accessibility**: WCAG 2.1 AA required. Min 4.5:1 contrast, visible focus rings, proper ARIA.
8. **Touch targets**: Min 48x48px, 8px gap between targets.
9. **Icons**: `<span class="material-symbols-rounded" aria-hidden="true">icon_name</span>`
10. **Buttons**: Always use `type="button"` on non-submit buttons.
11. **JavaScript**: ES2022+ modules, `const`/`let` only (never `var`), strict equality (`===`).

## File Locations

| Type | Location |
|------|----------|
| Blueprint assets | `blueprints/{name}/static/` |
| Blueprint templates | `blueprints/{name}/templates/{name}/` |
| Tests | `tests/unit/test_{blueprint}/` |
| Macros | `app/templates/macros/` |

## Documentation

- [UI/UX Guidelines](docs/uiux.md) - Design system, components, accessibility
- [Database Schema](docs/database-schema.md) - Table definitions, relationships
- [API Reference](docs/api.md) - RESTful API endpoints
- [Architecture](docs/architecture.md) - Blueprint structure, patterns
- [Components](docs/components.md) - Jinja2 macro library
- [PRD](docs/PRD.md) - Product requirements
