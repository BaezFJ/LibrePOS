# Installation Guide

This guide covers how to install and run LibrePOS for development or production use.

## Prerequisites

- Python 3.12 or higher
- Git
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Quick Start with uv (Recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package manager that handles virtual environments automatically.

### 1. Install uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### 2. Clone and install

```bash
git clone https://github.com/BaezFJ/LibrePOS.git
cd LibrePOS
```

### 3. Configure environment

```bash
cp librepos/.env.sample .env
```

Edit `.env` with your settings. See [Environment Configuration](ENVIRONMENT_CONFIGURATION.md) for details.

### 4. Install dependencies and initialize

```bash
# Install dependencies
uv sync

# Initialize database
uv run flask reset-db

# Seed permissions and test users
uv run flask seed-permissions
uv run flask create-test-users
```

### 5. Run the application

```bash
# Development server
uv run flask run

# Production server
uv run waitress-serve --port=5000 --call librepos:create_app
```

Visit http://127.0.0.1:5000

## Alternative: pip Installation

If you prefer using pip and venv:

```bash
# Clone repository
git clone https://github.com/BaezFJ/LibrePOS.git
cd LibrePOS

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Configure environment
cp librepos/.env.sample .env
# Edit .env with your settings

# Initialize database
flask reset-db
flask seed-permissions
flask create-test-users

# Run development server
flask run
```

## Test User Accounts

After running `flask create-test-users`, these accounts are available:

| Role | Email | Password |
|------|-------|----------|
| Owner | owner@librepos.com | librepos |
| Admin | admin@librepos.com | librepos |
| Manager | manager@librepos.com | librepos |
| Cashier | cashier@librepos.com | librepos |

**Change these credentials before deploying to production.**

## Production Setup

For production deployments:

### 1. Install with production dependencies

```bash
uv sync --extra prod
```

This includes `gunicorn` and `psycopg2-binary` for PostgreSQL.

### 2. Configure PostgreSQL

See [Database Configuration](DATABASE_CONFIGURATION.md) for PostgreSQL setup.

### 3. Set production environment variables

```bash
# .env
FLASK_ENV=production
SECRET_KEY=your-secure-random-key
SQLALCHEMY_DATABASE_URI=postgresql://user:pass@localhost:5432/librepos
```

Generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Run with Gunicorn

```bash
uv run gunicorn --bind 0.0.0.0:8000 --workers 4 "librepos:create_app()"
```

## Verifying Installation

After starting the server, verify everything is working:

1. Open http://127.0.0.1:5000 in your browser
2. Log in with one of the test accounts
3. Navigate to the dashboard

## Troubleshooting

**"Command not found: flask"**
- Ensure your virtual environment is activated
- With uv, use `uv run flask` instead of `flask`

**Database errors on startup**
- Run `flask reset-db` to recreate tables
- Check your `SQLALCHEMY_DATABASE_URI` in `.env`

**Permission errors**
- Run `flask seed-permissions` to sync permissions
- Run `flask sync-permissions` if you've added new permissions

## Next Steps

- [Environment Configuration](ENVIRONMENT_CONFIGURATION.md) - Configure environment variables
- [Database Configuration](DATABASE_CONFIGURATION.md) - Set up PostgreSQL or MySQL
- [README](README.md) - Development commands and project structure
