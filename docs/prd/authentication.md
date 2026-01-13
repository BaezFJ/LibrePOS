# Authentication Strategy

> Web authentication, API authentication, and model organization

---

## Web Authentication (Flask-Login)

- Session-based authentication using Flask-Login
- PIN entry support for quick staff switching at terminals
- Configurable session timeout based on user role
- Manager override workflow for sensitive operations

---

## API Authentication (JWT-Ready)

- Separate `@api_auth_required` decorator designed for JWT migration
- Token endpoint stubbed at `/api/v1/auth/token` for future implementation
- Refresh token support architecture planned
- API key authentication for third-party integrations

---

## Model Organization

| Model | Blueprint | Purpose |
|-------|-----------|---------|
| User | staff | Employee data and credentials |
| ActiveSession | auth | Session management |
| LoginAttempt | auth | Login tracking and rate limiting |
| APIKey | auth | Third-party integration keys |
| RefreshToken | auth | Future JWT refresh tokens |

The User model resides in the staff blueprint as it contains employee data. Session management models reside in the auth blueprint.
