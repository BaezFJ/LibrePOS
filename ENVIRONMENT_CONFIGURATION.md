# Environment Configuration Guide for LibrePOS

This guide explains how to configure environment variables for LibrePOS. Proper configuration is essential for both
development and production environments.

## Initial Setup
Create a `.env` file in the root directory of your project. (After step 1 and before step 4 if cloning from GitHub) This file will store your environment-specific configuration
values.


## Environment Variables Overview

LibrePOS uses the following environment variables for configuration:

### Core Settings

- `SECRET_KEY`: Required for session security (required in production)
- `DEBUG`: Enable debug mode (default: False)
- `TESTING`: Enable testing mode (default: False)

### Database Configuration

- `DATABASE_URL`: Database connection string (default: SQLite database in the application directory)
- `SQLALCHEMY_TRACK_MODIFICATIONS`: Track SQL Alchemy modifications (default: False)

### Email Configuration

- `MAIL_SERVER`: SMTP server address
- `MAIL_PORT`: SMTP server port
- `MAIL_USERNAME`: SMTP username
- `MAIL_PASSWORD`: SMTP password
- `MAIL_USE_TLS`: Enable TLS (default: False)
- `MAIL_USE_SSL`: Enable SSL (default: False)
- `MAIL_DEFAULT_SENDER`: Default sender email
- `MAIL_SUPPRESS_SEND`: Suppress email sending (default: False)
