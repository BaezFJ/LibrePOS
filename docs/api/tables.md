# Tables API

> Floor plans, table management, reservations, and waitlist

**Base URL:** `/api/v1`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tables/floor-plans/{id}` | Get floor plan with tables |
| GET | `/tables` | List tables |
| POST | `/tables/{id}/seat` | Seat party at table |
| PATCH | `/tables/{id}/status` | Update table status |
| GET | `/reservations` | List reservations |
| POST | `/reservations` | Create reservation |
| GET | `/waitlist` | Get current waitlist |
| POST | `/waitlist/{id}/notify` | Notify waitlist party |

---

## GET `/tables/floor-plans/{id}`

Retrieve floor plan layout with all tables and their current status.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Floor plan ID |

**Success Response (200):**

```json
{
  "id": 1,
  "name": "Main Floor",
  "tables": [
    {
      "id": 12,
      "table_number": "12",
      "capacity_max": 4,
      "x_position": 250,
      "y_position": 180,
      "shape": "square",
      "status": {
        "status": "seated",
        "party_size": 4,
        "server_name": "Sarah M."
      }
    }
  ]
}
```

---

## GET `/tables`

Retrieve all tables with current status.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | Filter by status |
| `section_id` | integer | No | Filter by section |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | List of tables with status |

---

## POST `/tables/{id}/seat`

Seat a party and create a new order.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Table ID |

**Request Body:**

```json
{
  "party_size": 4,
  "server_id": 5,
  "reservation_id": 128
}
```

**Success Response (200):**

```json
{
  "order_id": 1248,
  "table_status": {
    "status": "seated",
    "party_size": 4
  }
}
```

---

## PATCH `/tables/{id}/status`

Update the status of a table (e.g., dirty, available).

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Table ID |

**Request Body:**

```json
{
  "status": "dirty"
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Status updated |

---

## GET `/reservations`

Retrieve reservations for a specific date.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `date` | date | No | Filter by date |
| `status` | string | No | Filter: booked, confirmed, seated, no_show, cancelled |

**Success Response (200):**

```json
{
  "data": [
    {
      "id": 128,
      "customer_name": "Smith",
      "party_size": 4,
      "reservation_time": "2026-01-04T19:00:00Z",
      "status": "confirmed",
      "table_id": 12
    }
  ]
}
```

---

## POST `/reservations`

Create a new reservation.

**Authentication Required:** Yes

**Request Body:**

```json
{
  "customer_name": "Johnson",
  "phone": "555-0123",
  "party_size": 6,
  "reservation_time": "2026-01-05T19:30:00Z",
  "notes": "Anniversary dinner"
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 201 | Reservation created |

---

## GET `/waitlist`

Retrieve active waitlist entries.

**Authentication Required:** Yes

**Success Response (200):**

```json
{
  "data": [
    {
      "id": 45,
      "customer_name": "Williams",
      "party_size": 2,
      "quoted_wait_minutes": 20,
      "check_in_time": "2026-01-04T18:45:00Z",
      "status": "waiting"
    }
  ]
}
```

---

## POST `/waitlist/{id}/notify`

Send SMS notification that table is ready.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Waitlist entry ID |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Notification sent |
