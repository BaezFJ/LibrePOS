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
cp .env.sample .env
```

Edit `.env` with your settings. See [Environment Configuration](environment.md) for details.

### 4. Install dependencies and initialize

```bash
# Install dependencies
uv sync

# Run database migrations
uv run flask db upgrade

# Seed sample data (optional)
uv run flask seed all
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
cp .env.sample .env
# Edit .env with your settings

# Run database migrations
flask db upgrade

# Seed sample data (optional)
flask seed all

# Run development server
flask run
```

## Production Setup

For production deployments:

### 1. Install with production dependencies

```bash
uv sync --extra prod
```

This includes `gunicorn` and `psycopg2-binary` for PostgreSQL.

### 2. Configure PostgreSQL

See [Database Configuration](database.md) for PostgreSQL setup.

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
2. You should see the welcome page or login screen

## Troubleshooting

**"Command not found: flask"**
- Ensure your virtual environment is activated
- With uv, use `uv run flask` instead of `flask`

**Database errors on startup**
- Run `flask db upgrade` to apply migrations
- Check your `SQLALCHEMY_DATABASE_URI` in `.env`

**Migration errors**
- Ensure the database exists before running migrations
- For PostgreSQL/MySQL, create the database first: `CREATE DATABASE librepos;`

## Next Steps

- [Environment Configuration](environment.md) - Configure environment variables
- [Database Configuration](database.md) - Set up PostgreSQL or MySQL
- [README](../../README.md) - Development commands and project structure
