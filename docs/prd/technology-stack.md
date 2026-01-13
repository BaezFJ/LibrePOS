# Technology Stack

> Core framework, API, security, database, and utilities

---

## Core Framework

| Package | Purpose |
|---------|---------|
| Flask | Web framework with blueprint support |
| Flask-SQLAlchemy | ORM integration |
| Flask-Migrate | Database migration management via Alembic |
| Flask-Login | Session-based authentication |
| Flask-WTF | Form handling and CSRF protection |
| python-dotenv | Environment variable management |

---

## API and Serialization

| Package | Purpose |
|---------|---------|
| marshmallow | Object serialization and validation |
| flask-marshmallow | Flask integration for marshmallow |
| marshmallow-sqlalchemy | SQLAlchemy model serialization |

---

## Security

| Package | Purpose |
|---------|---------|
| Flask-Bcrypt | Password hashing |
| PyJWT | JSON Web Token support for API authentication |

---

## Database

| Package | Purpose |
|---------|---------|
| PostgreSQL | Primary database |
| psycopg2-binary | PostgreSQL driver |
| SQLAlchemy | ORM and database abstraction |

---

## Utilities

| Package | Purpose |
|---------|---------|
| python-dateutil | Advanced date and time handling |
| click | CLI framework (included with Flask) |

---

## Development Dependencies

| Package | Purpose |
|---------|---------|
| pytest | Testing framework |
| pytest-flask | Flask test fixtures |
| pytest-cov | Code coverage reporting |
| factory-boy | Test data generation |
| faker | Fake data generation |
| black | Code formatting |
| flake8 | Linting |
| isort | Import sorting |

---

## Frontend Libraries

| Library | Purpose |
|---------|---------|
| MaterializeCSS 2.2.2 | Material Design CSS framework |
| Chart.js | JavaScript charting for reports |
| SortableJS | Drag-and-drop reordering |
| interact.js | Drag, resize, and gesture handling |
