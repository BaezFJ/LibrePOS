# Inventory API

> Stock management, recipes, vendors, and purchase orders

**Base URL:** `/api/v1`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory/items` | List inventory items |
| POST | `/inventory/items/{id}/adjust` | Adjust stock level |
| GET | `/inventory/vendors` | List vendors |
| POST | `/inventory/purchase-orders` | Create purchase order |
| POST | `/inventory/purchase-orders/{id}/receive` | Receive items from PO |

---

## GET `/inventory/items`

Retrieve inventory items with stock levels.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `category` | string | No | Filter: protein, produce, dairy, dry_goods, beverage, paper |
| `low_stock` | boolean | No | Only items below reorder point |

**Success Response (200):**

```json
{
  "data": [
    {
      "id": 101,
      "name": "Ground Beef",
      "sku": "PRO-001",
      "category": "protein",
      "unit_of_measure": "lb",
      "quantity_on_hand": 45.5,
      "par_level": 50,
      "reorder_point": 20
    }
  ]
}
```

---

## POST `/inventory/items/{id}/adjust`

Record a stock adjustment with reason.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Item ID |

**Request Body:**

```json
{
  "adjustment_type": "waste",
  "quantity_change": -2.5,
  "reason": "Spoilage"
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Stock adjusted |

---

## GET `/inventory/vendors`

Retrieve vendor/supplier list.

**Authentication Required:** Yes

**Success Response (200):**

```json
{
  "data": [
    {
      "id": 1,
      "name": "Sysco",
      "contact_name": "John Rep",
      "phone": "555-0100",
      "payment_terms": "Net 30"
    }
  ]
}
```

---

## POST `/inventory/purchase-orders`

Create a new purchase order to a vendor.

**Authentication Required:** Yes

**Request Body:**

```json
{
  "vendor_id": 1,
  "expected_date": "2026-01-06",
  "line_items": [
    {
      "inventory_item_id": 101,
      "quantity_ordered": 50,
      "unit_cost": 4.25
    }
  ]
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 201 | Purchase order created |

---

## POST `/inventory/purchase-orders/{id}/receive`

Record received items against a purchase order.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | PO ID |

**Request Body:**

```json
{
  "line_items": [
    {
      "line_item_id": 1,
      "quantity_received": 48
    }
  ]
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Items received and stock updated |
