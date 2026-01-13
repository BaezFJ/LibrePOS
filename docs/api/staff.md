# Staff API

> Manage employees, roles, permissions, time tracking, and scheduling

**Base URL:** `/api/v1`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/staff/users` | List employees |
| POST | `/staff/users` | Create employee |
| POST | `/staff/clock-in` | Clock in |
| POST | `/staff/clock-out` | Clock out |
| GET | `/staff/roles` | List roles |
| GET | `/staff/time-entries` | List time entries |

---

## GET `/staff/users`

Retrieve paginated list of employees with filtering.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `role_id` | integer | No | Filter by role |
| `include_inactive` | boolean | No | Include inactive employees |

**Success Response (200):**

```json
{
  "data": [
    {
      "id": 1,
      "employee_number": "EMP001",
      "first_name": "John",
      "last_name": "Doe",
      "role": {
        "id": 3,
        "name": "Server"
      },
      "is_active": true
    }
  ]
}
```

---

## POST `/staff/users`

Create a new employee account.

**Authentication Required:** Yes

**Request Body:**

```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith@restaurant.com",
  "role_id": 3,
  "pin": "1234",
  "hire_date": "2026-01-04",
  "hourly_rate": 15.00
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 201 | Employee created |

---

## POST `/staff/clock-in`

Record clock-in for the authenticated user.

**Authentication Required:** Yes

**Success Response (200):**

```json
{
  "id": 1542,
  "user_id": 1,
  "clock_in": "2026-01-04T16:00:00Z",
  "shift_id": 245
}
```

---

## POST `/staff/clock-out`

Record clock-out with tip declaration.

**Authentication Required:** Yes

**Request Body:**

```json
{
  "cash_tips": 45.00,
  "credit_tips": 125.50
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Clocked out with tips declared |

---

## GET `/staff/roles`

Retrieve all roles with their permissions.

**Authentication Required:** Yes

**Success Response (200):**

```json
{
  "data": [
    {
      "id": 1,
      "name": "Admin",
      "is_system_role": true,
      "permissions": ["*"]
    },
    {
      "id": 3,
      "name": "Server",
      "is_system_role": true,
      "permissions": ["create_order", "process_payment", "view_menu"]
    }
  ]
}
```

---

## GET `/staff/time-entries`

Retrieve time entries for payroll and reporting.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | integer | No | Filter by employee |
| `date_from` | date | No | Start date |
| `date_to` | date | No | End date |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | List of time entries |
