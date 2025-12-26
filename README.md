# LibrePOS

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.x-green.svg)](https://flask.palletsprojects.com/)
[![Development Status](https://img.shields.io/badge/status-early%20development-orange.svg)]()

LibrePOS is a **free and open-source** web-based Point of Sale system designed for **restaurants** and **mobile food vendors**. Built with Python and Flask, it aims to provide small businesses with a cost-effective, flexible, and modern POS solution.

> **Note:** This project is in early development. Core infrastructure is in place, with business features actively being built.

## Current Status

### Implemented

- **Authentication System** - User login/logout with session management
- **Role-Based Access Control (RBAC)** - Granular permissions with policy-based authorization
- **User Management** - Create, edit, and manage users with role assignments
- **Staff Management** - Employee profiles and staff directory
- **Blueprint Architecture** - Modular, extensible codebase structure
- **CLI Tools** - Database management, user seeding, and permission syncing

### In Progress

See [POS_FEATURES.md](POS_FEATURES.md) for the complete feature roadmap, including:
- Order Management
- Menu Management
- Table Management
- Inventory Tracking
- Kitchen Display System
- Reporting & Analytics

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.12+, Flask 3.x |
| Database | SQLAlchemy 2.0 (SQLite for dev, PostgreSQL for production) |
| Authentication | Flask-Login |
| Forms | Flask-WTF, WTForms |
| Server | Waitress (dev), Gunicorn (production) |

## Quick Start

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended) or pip

### Installation

```bash
# Clone the repository
git clone https://github.com/BaezFJ/LibrePOS.git
cd LibrePOS

# Create environment file
cp librepos/.env.sample .env
# Edit .env with your configuration

# Install dependencies with uv
uv sync

# Initialize the database and seed permissions
uv run flask reset-db
uv run flask seed-permissions
uv run flask create-test-users

# Start the development server
uv run flask run
```

Visit `http://127.0.0.1:5000` in your browser.

### Default Test Users

After running `flask create-test-users`, these accounts are available:

| Role | Email | Password |
|------|-------|----------|
| Owner | owner@librepos.com | librepos |
| Admin | admin@librepos.com | librepos |
| Manager | manager@librepos.com | librepos |
| Cashier | cashier@librepos.com | librepos |

**Important:** Change these credentials in production environments.

## Development

```bash
# Run tests with coverage
uv run pytest

# Lint and format code
uv run ruff check .
uv run ruff format .

# Type checking
uv run pyright

# Create a new blueprint
uv run flask create-bp <name>

# Sync permissions after code changes
uv run flask sync-permissions
```

## Project Structure

```
librepos/
├── app.py              # Application factory
├── config.py           # Environment configurations
├── extensions.py       # Flask extensions
├── cli.py              # CLI commands
├── iam/                # Identity & Access Management
├── main/               # Dashboard, error handlers
├── staff/              # Staff management
├── permissions/        # Permission registry
├── utils/              # Shared utilities
└── ui/                 # Templates and static assets
```

## Configuration

LibrePOS uses environment variables for configuration. See [ENVIRONMENT_CONFIGURATION.md](ENVIRONMENT_CONFIGURATION.md) for details.

For database setup with PostgreSQL, MySQL, or other backends, see [DATABASE_CONFIGURATION.md](DATABASE_CONFIGURATION.md).

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run tests and linting (`pytest && ruff check .`)
5. Commit your changes (`git commit -m "Add your feature"`)
6. Push to the branch (`git push origin feature/your-feature`)
7. Open a Pull Request

## License

LibrePOS is licensed under the [GNU General Public License v3.0](LICENSE). You are free to use, modify, and distribute this software, provided that derivative works remain open source under the same license.

## Support

- **Issues:** [GitHub Issues](https://github.com/BaezFJ/LibrePOS/issues)
- **Discussions:** [GitHub Discussions](https://github.com/BaezFJ/LibrePOS/discussions)

---

Built with Flask for the food service industry.