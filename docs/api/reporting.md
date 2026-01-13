# Reporting API

> Sales reports, analytics, labor reports, and audit logs

**Base URL:** `/api/v1`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/reports/daily-summary` | Get daily summary |
| GET | `/reports/sales` | Get sales report |
| GET | `/reports/product-mix` | Get product mix report |
| GET | `/reports/labor` | Get labor report |
| GET | `/reports/audit-log` | Get audit log |

---

## GET `/reports/daily-summary`

Retrieve comprehensive daily business metrics.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `date` | date | Yes | Business date |

**Success Response (200):**

```json
{
  "business_date": "2026-01-04",
  "gross_sales": 8547.25,
  "net_sales": 7892.50,
  "tax_collected": 651.63,
  "discounts_given": 425.00,
  "tips_collected": 1284.75,
  "order_count": 156,
  "guest_count": 412,
  "average_check": 50.59,
  "labor_hours": 85.5,
  "labor_cost": 1282.50,
  "labor_percentage": 16.25
}
```

---

## GET `/reports/sales`

Retrieve sales data with flexible grouping.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `date_from` | date | Yes | Start date |
| `date_to` | date | Yes | End date |
| `group_by` | string | No | Group by: hour, day, week, month |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Sales report data |

---

## GET `/reports/product-mix`

Retrieve item sales by quantity and revenue.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `date_from` | date | Yes | Start date |
| `date_to` | date | Yes | End date |
| `category_id` | integer | No | Filter by category |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Product mix data |

---

## GET `/reports/labor`

Retrieve labor hours and costs.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `date_from` | date | Yes | Start date |
| `date_to` | date | Yes | End date |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Labor report data |

---

## GET `/reports/audit-log`

Retrieve system audit trail for sensitive actions.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | integer | No | Filter by user |
| `action` | string | No | Filter by action type |
| `date_from` | datetime | No | Start datetime |

**Success Response (200):**

```json
{
  "data": [
    {
      "id": 8521,
      "user_id": 1,
      "user_name": "John Doe",
      "action": "void_order",
      "entity_type": "order",
      "entity_id": 1247,
      "created_at": "2026-01-04T19:15:00Z"
    }
  ]
}
```
