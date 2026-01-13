# Customers API

> Customer profiles, loyalty program, gift cards, and feedback

**Base URL:** `/api/v1`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/customers` | List customers |
| GET | `/customers/lookup` | Lookup customer |
| GET | `/loyalty/accounts/{id}` | Get loyalty account |
| POST | `/loyalty/redeem` | Redeem reward |
| GET | `/gift-cards/{card_number}` | Check gift card balance |
| POST | `/gift-cards/{card_number}/redeem` | Redeem gift card |

---

## GET `/customers`

Search and list customer profiles.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `search` | string | No | Search by name, email, or phone |

**Success Response (200):**

```json
{
  "data": [
    {
      "id": 501,
      "first_name": "Jane",
      "last_name": "Smith",
      "email": "jane@email.com",
      "phone": "555-0199",
      "total_orders": 24,
      "total_spent": 1250.00
    }
  ]
}
```

---

## GET `/customers/lookup`

Quick lookup by phone or email.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `phone` | string | No | Phone number |
| `email` | string | No | Email address |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Customer found |
| 404 | Customer not found |

---

## GET `/loyalty/accounts/{id}`

Retrieve loyalty account details including points and tier.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Loyalty account ID |

**Success Response (200):**

```json
{
  "id": 301,
  "customer_id": 501,
  "tier": {
    "id": 2,
    "name": "Silver",
    "multiplier": 1.25
  },
  "points_balance": 2450,
  "lifetime_points": 8500
}
```

---

## POST `/loyalty/redeem`

Redeem points for a reward.

**Authentication Required:** Yes

**Request Body:**

```json
{
  "loyalty_account_id": 301,
  "reward_id": 5,
  "check_id": 1247
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Reward redeemed |

---

## GET `/gift-cards/{card_number}`

Retrieve gift card balance and status.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `card_number` | string | Yes | Gift card number |

**Success Response (200):**

```json
{
  "card_number": "GC-1234-5678",
  "current_balance": 50.00,
  "status": "active"
}
```

---

## POST `/gift-cards/{card_number}/redeem`

Use gift card balance toward payment.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `card_number` | string | Yes | Gift card number |

**Request Body:**

```json
{
  "amount": 25.00,
  "pin": "1234"
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Gift card redeemed |
