# Authentication API

> User authentication, session management, and token handling

**Base URL:** `/api/v1`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Authenticate user |
| POST | `/auth/logout` | End session |
| POST | `/auth/refresh` | Refresh access token |
| GET | `/auth/me` | Get current user info |

---

## POST `/auth/login`

Authenticate user with PIN or password credentials. Returns access token and user details.

**Authentication Required:** No

**Request Body (PIN-based):**

```json
{
  "employee_number": "EMP001",
  "pin": "1234"
}
```

**Request Body (Password-based):**

```json
{
  "email": "manager@restaurant.com",
  "password": "securepassword"
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Login successful |
| 401 | Invalid credentials |
| 429 | Too many login attempts |

**Success Response (200):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "role": "Server"
  }
}
```

---

## POST `/auth/logout`

Invalidate the current session and access token.

**Authentication Required:** Yes

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Logout successful |

**Success Response (200):**

```json
{
  "message": "Successfully logged out"
}
```

---

## POST `/auth/refresh`

Exchange a valid refresh token for a new access token.

**Authentication Required:** No

**Request Body:**

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Token refreshed |
| 401 | Invalid refresh token |

---

## GET `/auth/me`

Retrieve the profile and permissions of the currently authenticated user.

**Authentication Required:** Yes

**Success Response (200):**

```json
{
  "id": 1,
  "employee_number": "EMP001",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@restaurant.com",
  "role": {
    "id": 3,
    "name": "Server",
    "permissions": ["create_order", "process_payment"]
  }
}
```
