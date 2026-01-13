# Payments API

> Process payments, manage tips, discounts, and cash drawers

**Base URL:** `/api/v1`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/payments/process` | Process payment |
| POST | `/payments/{id}/void` | Void payment |
| POST | `/payments/{id}/refund` | Refund payment |
| POST | `/payments/{id}/tip` | Add/adjust tip |
| POST | `/checks/{id}/discount` | Apply discount to check |
| GET | `/discounts` | List available discounts |
| POST | `/cash-drawers/{id}/open` | Open cash drawer |
| POST | `/cash-drawers/{id}/close` | Close and count cash drawer |

---

## POST `/payments/process`

Process a payment against a check. Supports card, cash, gift card, and mobile wallet.

**Authentication Required:** Yes

**Request Body:**

```json
{
  "check_id": 1247,
  "amount": 84.25,
  "tender_type": "credit",
  "tip_amount": 15.17,
  "card_token": "tok_visa_4242"
}
```

**Success Response (200):**

```json
{
  "payment": {
    "id": 5621,
    "amount": 84.25,
    "tip_amount": 15.17,
    "status": "captured",
    "reference_number": "TXN-20260104-5621"
  },
  "check": {
    "id": 1247,
    "status": "paid",
    "total": 84.25
  },
  "authorization_code": "AUTH123456"
}
```

**Error Response (402):**

```json
{
  "error": "payment_declined",
  "message": "Card declined",
  "decline_code": "insufficient_funds"
}
```

---

## POST `/payments/{id}/void`

Void a payment before batch settlement. Requires manager authorization.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Payment ID |

**Request Body:**

```json
{
  "reason": "Wrong amount charged",
  "manager_pin": "9999"
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Payment voided |

---

## POST `/payments/{id}/refund`

Process a full or partial refund. Requires manager authorization.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Payment ID |

**Request Body:**

```json
{
  "amount": 25.00,
  "reason": "Food quality issue",
  "manager_pin": "9999"
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Refund processed |

---

## POST `/payments/{id}/tip`

Add or adjust tip amount on a processed payment.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Payment ID |

**Request Body:**

```json
{
  "amount": 15.17
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Tip adjusted |

---

## POST `/checks/{id}/discount`

Apply a discount by ID or promo code. Some discounts require manager authorization.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Check ID |

**Request Body:**

```json
{
  "discount_id": 5,
  "manager_pin": "9999"
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Discount applied |

---

## GET `/discounts`

Retrieve all active discounts available for application.

**Authentication Required:** Yes

**Success Response (200):**

```json
{
  "data": [
    {
      "id": 1,
      "name": "Happy Hour",
      "discount_type": "percentage",
      "value": 20,
      "requires_authorization": false
    },
    {
      "id": 2,
      "name": "Manager Comp",
      "discount_type": "percentage",
      "value": 100,
      "requires_authorization": true
    }
  ]
}
```

---

## POST `/cash-drawers/{id}/open`

Open a cash drawer with starting amount for a shift.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Drawer ID |

**Request Body:**

```json
{
  "opening_amount": 200.00
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Drawer opened |

---

## POST `/cash-drawers/{id}/close`

Close drawer with counted amount. System calculates variance.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Drawer ID |

**Request Body:**

```json
{
  "counted_amount": 847.50,
  "variance_reason": null
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Drawer closed with reconciliation |
