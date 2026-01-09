# Environment Configuration

LibrePOS uses environment variables for configuration. This guide covers all available settings and common configurations.

## Quick Start

Create a `.env` file in the project root:

```bash
cp .env.sample .env
```

### Minimal Development Config

For local development, you only need:

```bash
# .env
SECRET_KEY=dev-secret-key-change-in-production
DEBUG=True
```

SQLite is used by default if no database URL is set.

### Minimal Production Config

```bash
# .env
SECRET_KEY=your-secure-random-key-here
DEBUG=False
SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost:5432/librepos
```

Generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Environment Variables Reference

### Core Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Session encryption key | None | Yes (production) |
| `DEBUG` | Enable debug mode | `False` | No |
| `TESTING` | Enable testing mode | `False` | No |

### Database

| Variable | Description | Default |
|----------|-------------|---------|
| `SQLALCHEMY_DATABASE_URI` | SQLAlchemy connection URI | `sqlite:///librepos.db` |

See [Database Configuration](database.md) for connection string formats.

### Email (Flask-Mailman)

| Variable | Description | Default |
|----------|-------------|---------|
| `MAIL_SERVER` | SMTP server hostname | None |
| `MAIL_PORT` | SMTP server port | `587` |
| `MAIL_USERNAME` | SMTP authentication username | None |
| `MAIL_PASSWORD` | SMTP authentication password | None |
| `MAIL_USE_TLS` | Use TLS encryption | `False` |
| `MAIL_USE_SSL` | Use SSL encryption | `False` |
| `MAIL_DEFAULT_SENDER` | Default "From" address | None |
| `MAIL_SUPPRESS_SEND` | Disable email sending | `False` |

## Configuration Examples

### Development

```bash
# .env
SECRET_KEY=dev-key-not-for-production
DEBUG=True
TESTING=False

# Uses SQLite by default (no SQLALCHEMY_DATABASE_URI needed)

# Suppress emails during development
MAIL_SUPPRESS_SEND=True
```

### Production

```bash
# .env
SECRET_KEY=a1b2c3d4e5f6...  # Use generated key
DEBUG=False
TESTING=False

# PostgreSQL database
SQLALCHEMY_DATABASE_URI=postgresql://librepos:strongpassword@localhost:5432/librepos

# Email configuration
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=noreply@example.com
MAIL_PASSWORD=smtp-password
MAIL_USE_TLS=True
MAIL_DEFAULT_SENDER="LibrePOS <noreply@example.com>"
```

### Gmail SMTP

```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_USE_TLS=True
MAIL_DEFAULT_SENDER="LibrePOS <your-email@gmail.com>"
```

> **Note:** Gmail requires an [App Password](https://support.google.com/accounts/answer/185833) if 2FA is enabled.

### SendGrid

```bash
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
MAIL_USE_TLS=True
MAIL_DEFAULT_SENDER="LibrePOS <noreply@yourdomain.com>"
```

### Mailgun

```bash
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USERNAME=postmaster@your-domain.mailgun.org
MAIL_PASSWORD=your-mailgun-password
MAIL_USE_TLS=True
MAIL_DEFAULT_SENDER="LibrePOS <noreply@your-domain.mailgun.org>"
```

## Security Notes

1. **Never commit `.env` to version control** - It's already in `.gitignore`

2. **Use strong secret keys in production** - Generate with:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Use environment-specific files** - Consider `.env.development` and `.env.production`

4. **Restrict file permissions** - On Linux/macOS:
   ```bash
   chmod 600 .env
   ```

## Troubleshooting

**"SECRET_KEY not set" error**
- Ensure `.env` file exists in project root
- Check the variable name is exactly `SECRET_KEY`

**Database connection errors**
- Verify `SQLALCHEMY_DATABASE_URI` format matches your database type
- Check database server is running and accessible

**Emails not sending**
- Check `MAIL_SUPPRESS_SEND` is not `True`
- Verify SMTP credentials are correct
- Check firewall allows outbound connections on mail port
