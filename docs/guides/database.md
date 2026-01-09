# Database Configuration

LibrePOS uses SQLAlchemy and supports multiple database backends. This guide covers how to configure your database connection.

## Quick Reference

| Database | Use Case | URI Format |
|----------|----------|------------|
| SQLite | Development, small deployments | `sqlite:///librepos.db` |
| PostgreSQL | Production (recommended) | `postgresql://user:pass@host:5432/db` |
| MySQL | Production (alternative) | `mysql+pymysql://user:pass@host:3306/db` |

## SQLite (Default)

SQLite requires no additional setup and is ideal for development or single-user deployments.

```bash
# .env
SQLALCHEMY_DATABASE_URI=sqlite:///librepos.db
```

The database file is created automatically. No drivers needed.

## PostgreSQL (Recommended for Production)

PostgreSQL is the recommended database for production deployments.

### 1. Install the driver

```bash
# With uv (includes psycopg2-binary)
uv sync --extra prod

# Or with pip
pip install psycopg2-binary
```

### 2. Configure the connection

```bash
# .env
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost:5432/librepos
```

### Example

```bash
# Local PostgreSQL with user 'postgres', password 'secret', database 'librepos'
SQLALCHEMY_DATABASE_URI=postgresql://postgres:secret@localhost:5432/librepos

# Remote server
SQLALCHEMY_DATABASE_URI=postgresql://librepos_user:strongpass@db.example.com:5432/librepos_prod
```

## MySQL / MariaDB

### 1. Install the driver

```bash
uv add pymysql
# or
pip install pymysql
```

### 2. Configure the connection

```bash
# .env
SQLALCHEMY_DATABASE_URI=mysql+pymysql://username:password@localhost:3306/librepos
```

## Initializing the Database

After configuring your connection, initialize the database:

```bash
# Run database migrations
uv run flask db upgrade

# Seed sample data (optional)
uv run flask seed all
```

## Connection String Format

The general format for SQLAlchemy database URIs:

```
dialect+driver://username:password@host:port/database
```

| Component | Description |
|-----------|-------------|
| `dialect` | Database type (postgresql, mysql, sqlite) |
| `driver` | Python driver (optional, e.g., pymysql) |
| `username` | Database user |
| `password` | Database password (URL-encode special characters) |
| `host` | Server hostname or IP |
| `port` | Server port |
| `database` | Database name |

### Special Characters in Passwords

If your password contains special characters, URL-encode them:

| Character | Encoded |
|-----------|---------|
| `@` | `%40` |
| `:` | `%3A` |
| `/` | `%2F` |
| `#` | `%23` |

Example: password `p@ss:word` becomes `p%40ss%3Aword`

## Troubleshooting

**Connection refused**
- Verify the database server is running
- Check host and port are correct
- Ensure firewall allows connections

**Authentication failed**
- Verify username and password
- Check the user has access to the specified database
- URL-encode special characters in password

**Driver not found**
- Install the appropriate Python driver package
- For PostgreSQL: `psycopg2-binary`
- For MySQL: `pymysql`

**Database does not exist**
- Create the database first: `CREATE DATABASE librepos;`
- SQLite creates the file automatically; others require manual creation

## Other Databases

LibrePOS can work with any SQLAlchemy-supported database. For Oracle or SQL Server, refer to the [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/20/core/engines.html).