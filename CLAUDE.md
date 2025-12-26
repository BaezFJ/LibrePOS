# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LibrePOS is a Flask-based web Point of Sale (POS) system for restaurants and mobile food vendors. It uses Flask 3.x with SQLAlchemy 2.0, Flask-Login for authentication, and Flask-WTF for forms.

## Common Commands

```bash
# Run development server
flask run

# Run tests with coverage
pytest

# Run a single test file
pytest tests/test_example.py

# Run tests matching a pattern
pytest -k "test_user"

# Lint and format code
ruff check .
ruff format .

# Type checking
pyright

# CLI commands for development
flask create-bp <name>       # Scaffold a new blueprint
flask add-superuser          # Create a superuser interactively
flask create-test-users      # Seed test users (owner, admin, manager, cashier, etc.)
flask seed-permissions       # Auto-discover and seed permissions from blueprints
flask sync-permissions       # Sync DB permissions with code definitions
flask reset-db               # Drop and recreate all tables
```

## Architecture

### Application Factory Pattern
Entry point is `wsgi.py` → `create_app()` in `librepos/app.py`. Extensions are initialized in `librepos/extensions.py`.

### Blueprint Structure
Each feature module follows a consistent structure:
```
librepos/{blueprint}/
├── models.py        # SQLAlchemy models
├── routes.py        # Blueprint registration
├── views.py         # View functions
├── forms.py         # WTForms definitions
├── permissions.py   # StrEnum permissions + PolicyDefinition
├── decorators.py    # Route decorators (optional)
└── templates/{blueprint}/
```

Blueprints are auto-registered via `librepos/main/routes.py::register_blueprints()`.

### Database Models
All models inherit from `BaseModel` (provides id + timestamps) and `CRUDMixin` (provides `get_by_id`, `get_all`, `create`, `save`, `update`, `delete` methods).

Junction tables use `AssociationModel` (timestamps only, no id).

### Permission System
Permissions are defined as `StrEnum` classes in each blueprint's `permissions.py`. The `PermissionRegistry` auto-discovers these and `PermissionSeeder` creates DB records.

Use `@permission_required(PermissionName.SOME_PERMISSION)` decorator to protect routes.

### Key Modules
- `librepos/iam/` - Identity and Access Management (users, roles, permissions, policies)
- `librepos/main/` - Dashboard, error handlers
- `librepos/permissions/` - Central permission registry and seeding
- `librepos/utils/` - Shared utilities (CRUDMixin, forms, datetime, money)
- `librepos/ui/` - Shared templates and static assets

### Configuration
Environment-based configs in `librepos/config.py`: `DevelopmentConfig`, `TestingConfig`, `ProductionConfig`. Uses `.env` for environment variables.

### Templates
Base layout at `ui/templates/base.html`. Reusable Jinja2 macros in `ui/templates/components/`. Each blueprint has templates at `{blueprint}/templates/{blueprint}/`.
