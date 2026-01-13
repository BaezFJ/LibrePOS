# Database & Migrations

> Migration structure, commands, and cross-blueprint model imports.

---

## Migration Directory

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

---

## Common Commands

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

---

## Cross-Blueprint Model Imports

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
