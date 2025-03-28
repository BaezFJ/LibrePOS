# Database Configuration Guide for LibrePOS

This document explains how to connect LibrePOS to various databases using `Flask-SQLAlchemy`. You’ll learn how to set up your **environment file** (`.env`) and configure the SQLAlchemy URI for different database systems.

> **Note**: This guide does not cover installing the databases themselves. It focuses solely on configuring the application to connect to an existing database.

---

## Prerequisites

- Ensure that your desired database system is installed and running.
- Use the correct database credentials when setting up your `.env` file.

LibrePOS uses the `SQLALCHEMY_DATABASE_URI` setting from the `.env` file to connect to the database. Below are connection configurations for the most common database systems.

---

## 1. PostgreSQL

To use PostgreSQL, configure your `.env` file as follows:

```plaintext
SQLALCHEMY_DATABASE_URI=postgresql://username:password@host:port/database_name
```

### Example:
If your PostgreSQL server is running on `localhost` with:
- Username: `postgres`
- Password: `securepassword`
- Port: `5432`
- Database name: `librepos`

Your `.env` file should look like this:

```plaintext
SQLALCHEMY_DATABASE_URI=postgresql://postgres:securepassword@localhost:5432/librepos
```

---

## 2. MySQL

To use MySQL, configure your `.env` file as follows:

```plaintext
SQLALCHEMY_DATABASE_URI=mysql+pymysql://username:password@host:port/database_name
```

### Example:
If your MySQL server is running on `localhost` with:
- Username: `root`
- Password: `securepassword`
- Port: `3306`
- Database name: `librepos`

Your `.env` file should look like this:

```plaintext
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:securepassword@localhost:3306/librepos
```

> **Note**: Install the `pymysql` Python package for MySQL support by running:
> ```bash
> pip install pymysql
> ```

---

## 3. Oracle

To use Oracle, configure your `.env` file as follows:

```plaintext
SQLALCHEMY_DATABASE_URI=oracle+cx_oracle://username:password@host:port/?service_name=service_name
```

### Example:
If your Oracle instance is running on `192.168.1.100` with:
- Username: `admin`
- Password: `securepassword`
- Port: `1521`
- Service name: `xe`

Your `.env` file should look like this:

```plaintext
SQLALCHEMY_DATABASE_URI=oracle+cx_oracle://admin:securepassword@192.168.1.100:1521/?service_name=xe
```

> **Note**: Install the `cx_Oracle` package for Oracle support by running:
> ```bash
> pip install cx_Oracle
> ```

---

## 4. Microsoft SQL Server

To use Microsoft SQL Server, configure your `.env` file as follows:

```plaintext
SQLALCHEMY_DATABASE_URI=mssql+pyodbc://username:password@host:port/database_name?driver=ODBC+Driver+17+for+SQL+Server
```

### Example:
If your SQL Server instance is running on `localhost` with:
- Username: `sa`
- Password: `securepassword`
- Port: `1433`
- Database name: `librepos`

Your `.env` file should look like this:

```plaintext
SQLALCHEMY_DATABASE_URI=mssql+pyodbc://sa:securepassword@localhost:1433/librepos?driver=ODBC+Driver+17+for+SQL+Server
```

> **Note**:
> - Install the `pyodbc` Python package for SQL Server support by running:
> ```bash
> pip install pyodbc
> ```
> - Make sure the correct ODBC driver (e.g., `ODBC Driver 17 for SQL Server`) is installed on your system.

---

## 5. SQLite (Default for Development and Standalone Instances)

SQLite is lightweight and easy to use, making it ideal for standalone installations or during development. To use SQLite, configure your `.env` file as follows:

```plaintext
SQLALCHEMY_DATABASE_URI=sqlite:///absolute/path/to/your/database.db
```

### Example:
For a database file named `librepos.db` in your project folder, configure your `.env` file like this:

```plaintext
SQLALCHEMY_DATABASE_URI=sqlite:///librepos.db
```

SQLite doesn't require additional software installations or drivers. The database file will be created automatically if it doesn’t exist.

---

## Testing the Configuration

Once the database is configured, test the connection by running database migrations or starting the application.

### Example Command (for Flask-Migrate):
```bash
  flask db upgrade
```

If the configuration is correct, this command will connect to the database and apply migrations without errors.

---

## Troubleshooting

If you encounter connection issues:
1. Double-check the credentials and host information in your `.env` file.
2. Verify that your database server is running and accessible from your application’s host.
3. Ensure any necessary Python driver packages (e.g., `pymysql`, `cx_Oracle`, `pyodbc`) are installed.
4. Review the full error message for additional clues.

---

With the above configurations, LibrePOS can connect to and interact with a variety of databases using Flask-SQLAlchemy. Happy coding!