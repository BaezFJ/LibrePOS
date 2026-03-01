# Scripts

Utility scripts for developing and operating LibrePOS. Run all commands from the **project root**.

## create_blueprint.py

Scaffolds a new Flask blueprint with full boilerplate (routes, models, services, schemas, forms, permissions) and auto-registers it with the app factory.

### Prerequisites

The project's Python environment must be active with `click` installed (included in dev dependencies).

### Usage

```bash
# Interactive mode — prompts for name, prefix, description, and file selection
python scripts/create_blueprint.py

# Provide the name directly
python scripts/create_blueprint.py orders

# Fully non-interactive
python scripts/create_blueprint.py orders --prefix /orders --desc "Order management" -y

# Skip files you don't need
python scripts/create_blueprint.py orders --skip schemas --skip services

# Generate files without registering the blueprint in the app factory
python scripts/create_blueprint.py orders --no-register
```

### What it generates

```
src/librepos/app/blueprints/<name>/
├── __init__.py          # Blueprint definition (always created)
├── routes.py            # Route handlers with index/detail stubs
├── models.py            # SQLAlchemy model template
├── services.py          # Service class with CRUD method stubs
├── schemas.py           # Marshmallow schema template
├── forms.py             # WTForms template
├── permissions.py       # Permission enum and policy stubs
├── static/
│   ├── css/.gitkeep
│   └── js/.gitkeep
└── templates/<name>/
    └── index.html       # Jinja2 template extending layouts/admin.html
```

Unless `--no-register` is passed, the script also:

1. Adds a `from .<name> import bp` import to `blueprints/__init__.py`
2. Registers the blueprint inside `register_blueprints(app)`
3. Ensures `app/__init__.py` calls `register_blueprints()`

### After running

1. Edit `models.py` to define your database models
2. Run `flask db migrate -m "Add <name> models"`
3. Run `flask db upgrade`
4. Visit the blueprint's URL prefix to verify

## deploy.sh

Deployment script (placeholder — not yet implemented).

## seed_data.py

Database seeding script (placeholder — not yet implemented).
