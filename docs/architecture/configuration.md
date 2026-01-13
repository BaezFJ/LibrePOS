# Configuration Management

> Environment variables and configuration classes.

---

## Environment Variables (`.env`)

```bash
# Application
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/pos_dev

# Redis (sessions, caching)
REDIS_URL=redis://localhost:6379/0

# Authentication
SESSION_TIMEOUT_MINUTES=480
JWT_SECRET_KEY=your-jwt-secret

# Payment Gateway
PAYMENT_GATEWAY_API_KEY=pk_test_xxx
PAYMENT_GATEWAY_SECRET=sk_test_xxx

# Integrations
DOORDASH_API_KEY=xxx
UBEREATS_API_KEY=xxx
QUICKBOOKS_CLIENT_ID=xxx
```

---

## Configuration Classes (`app/config.py`)

```python
class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SESSION_COOKIE_SECURE = True
```
