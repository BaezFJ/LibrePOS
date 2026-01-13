# Orders API

> Create and manage orders, order items, and checks

**Base URL:** `/api/v1`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/orders` | List orders |
| POST | `/orders` | Create new order |
| GET | `/orders/{id}` | Get order by ID |
| POST | `/orders/{id}/items` | Add item to order |
| POST | `/orders/{id}/submit` | Submit order to kitchen |
| POST | `/orders/{id}/void` | Void entire order |
| POST | `/orders/{id}/checks` | Create/split check |

---

## GET `/orders`

Retrieve paginated list of orders with filtering options.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | Filter: draft, submitted, preparing, ready, completed, cancelled |
| `order_type` | string | No | Filter: dine_in, takeout, delivery, bar |
| `server_id` | integer | No | Filter by server |
| `table_id` | integer | No | Filter by table |
| `date_from` | date | No | Start date filter |
| `date_to` | date | No | End date filter |

**Success Response (200):**

```json
{
  "data": [
    {
      "id": 1247,
      "order_number": "ORD-1247",
      "order_type": "dine_in",
      "status": "preparing",
      "table_id": 12,
      "table_number": "12",
      "server_name": "Sarah M.",
      "guest_count": 4,
      "total": 84.25,
      "created_at": "2026-01-04T18:30:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 156,
    "total_pages": 8
  }
}
```

---

## POST `/orders`

Create a new order. For dine-in, specify table_id.

**Authentication Required:** Yes

**Request Body:**

```json
{
  "order_type": "dine_in",
  "table_id": 12,
  "guest_count": 4
}
```

**Success Response (201):**

```json
{
  "id": 1248,
  "order_number": "ORD-1248",
  "status": "draft",
  "created_at": "2026-01-04T19:00:00Z"
}
```

---

## GET `/orders/{id}`

Retrieve complete order details including items, checks, and payments.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Order ID |

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `include` | string | No | Comma-separated: items, checks, payments |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Order details with items and checks |
| 404 | Order not found |

---

## POST `/orders/{id}/items`

Add a menu item to an existing order.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Order ID |

**Request Body:**

```json
{
  "menu_item_id": 15,
  "quantity": 2,
  "modifier_ids": [2, 8],
  "notes": "Extra crispy",
  "course": "entree",
  "seat_number": 1
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 201 | Item added to order |

---

## POST `/orders/{id}/submit`

Send the order to kitchen for preparation. Creates kitchen tickets routed to appropriate stations.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Order ID |

**Request Body:**

```json
{
  "priority": "normal"
}
```

**Success Response (200):**

```json
{
  "message": "Order submitted to kitchen",
  "tickets_created": 3
}
```

---

## POST `/orders/{id}/void`

Void an order. Requires manager authorization.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Order ID |

**Request Body:**

```json
{
  "reason": "Guest walked out",
  "manager_pin": "9999"
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Order voided |
| 403 | Invalid manager authorization |

---

## POST `/orders/{id}/checks`

Create a new check or split existing check by seat, item, or amount.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Order ID |

**Request Body:**

```json
{
  "split_type": "by_seat",
  "seat_numbers": [1, 2]
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 201 | Check created |
