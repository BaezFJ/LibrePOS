# Integrations API

> Third-party integrations, webhooks, and external orders

**Base URL:** `/api/v1`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/integrations` | List integrations |
| POST | `/integrations/{id}/sync` | Trigger manual sync |
| GET | `/external-orders` | List external orders |
| POST | `/external-orders/{id}/accept` | Accept external order |
| POST | `/webhooks` | Create webhook endpoint |

---

## GET `/integrations`

Retrieve configured third-party integrations.

**Authentication Required:** Yes

**Success Response (200):**

```json
{
  "data": [
    {
      "id": 1,
      "name": "DoorDash",
      "integration_type": "delivery",
      "provider": "doordash",
      "is_active": true,
      "last_sync_at": "2026-01-04T18:00:00Z"
    },
    {
      "id": 2,
      "name": "QuickBooks",
      "integration_type": "accounting",
      "provider": "quickbooks",
      "is_active": true
    }
  ]
}
```

---

## POST `/integrations/{id}/sync`

Manually trigger a sync with the integration.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Integration ID |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Sync started |

---

## GET `/external-orders`

Retrieve orders from third-party platforms.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `integration_id` | integer | No | Filter by integration |
| `status` | string | No | Filter by status |

**Success Response (200):**

```json
{
  "data": [
    {
      "id": 891,
      "integration_id": 1,
      "external_id": "DD-12345",
      "status": "received",
      "raw_data": {
        "customer": "John D.",
        "items": []
      }
    }
  ]
}
```

---

## POST `/external-orders/{id}/accept`

Accept an incoming order from a delivery platform.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | External order ID |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Order accepted and injected to POS |

---

## POST `/webhooks`

Register a webhook to receive real-time events.

**Authentication Required:** Yes

**Request Body:**

```json
{
  "integration_id": 1,
  "url": "https://example.com/webhook",
  "events": ["order.created", "order.completed", "payment.completed"]
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 201 | Webhook created |
