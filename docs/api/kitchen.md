# Kitchen API

> Kitchen display system, ticket management, and station operations

**Base URL:** `/api/v1`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/kitchen/tickets` | List kitchen tickets |
| POST | `/kitchen/tickets/{id}/start` | Start cooking ticket |
| POST | `/kitchen/tickets/{id}/bump` | Bump/complete ticket |
| GET | `/kitchen/all-day` | Get all-day counts |
| GET | `/kitchen/stations` | List kitchen stations |

---

## GET `/kitchen/tickets`

Retrieve active kitchen tickets for KDS display.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `station_id` | integer | No | Filter by station |
| `status` | string | No | Filter: pending, in_progress, ready, bumped |
| `priority` | string | No | Filter: normal, rush, vip |

**Success Response (200):**

```json
{
  "data": [
    {
      "id": 4521,
      "order_id": 1247,
      "station_id": 1,
      "status": "in_progress",
      "priority": "normal",
      "items": [
        {
          "name": "Burger",
          "quantity": 2,
          "notes": "Med-rare"
        }
      ],
      "created_at": "2026-01-04T18:35:00Z",
      "elapsed_minutes": 8
    }
  ]
}
```

---

## POST `/kitchen/tickets/{id}/start`

Mark a ticket as in-progress (cooking started).

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Ticket ID |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Ticket started |

---

## POST `/kitchen/tickets/{id}/bump`

Mark ticket as complete and remove from active display.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Ticket ID |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Ticket bumped |

---

## GET `/kitchen/all-day`

Retrieve running totals of pending items across all tickets.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `station_id` | integer | No | Filter by station |

**Success Response (200):**

```json
{
  "items": [
    { "menu_item_id": 15, "name": "Burger", "count": 12 },
    { "menu_item_id": 22, "name": "Caesar Salad", "count": 5 }
  ]
}
```

---

## GET `/kitchen/stations`

Retrieve configured kitchen stations.

**Authentication Required:** Yes

**Success Response (200):**

```json
{
  "data": [
    { "id": 1, "name": "Grill", "station_type": "grill", "is_active": true },
    { "id": 2, "name": "Fry", "station_type": "fryer", "is_active": true },
    { "id": 3, "name": "Bar", "station_type": "bar", "is_active": true }
  ]
}
```
