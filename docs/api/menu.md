# Menu API

> Menu items, categories, modifiers, pricing rules, and availability

**Base URL:** `/api/v1`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/menu/categories` | List all categories |
| POST | `/menu/categories` | Create category |
| GET | `/menu/items` | List menu items |
| POST | `/menu/items` | Create menu item |
| GET | `/menu/items/{id}` | Get menu item by ID |
| PATCH | `/menu/items/{id}/availability` | Toggle item availability (86) |
| GET | `/menu/modifier-groups` | List modifier groups |

---

## GET `/menu/categories`

Retrieve all menu categories with optional filtering.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `include_inactive` | boolean | No | Include inactive categories |
| `parent_id` | integer | No | Filter by parent category |

**Success Response (200):**

```json
{
  "data": [
    {
      "id": 1,
      "name": "Appetizers",
      "description": "Starters and small plates",
      "display_order": 1,
      "is_active": true,
      "item_count": 12
    },
    {
      "id": 2,
      "name": "Entrees",
      "description": "Main courses",
      "display_order": 2,
      "is_active": true,
      "item_count": 18
    }
  ]
}
```

---

## POST `/menu/categories`

Create a new menu category.

**Authentication Required:** Yes

**Request Body:**

```json
{
  "name": "Desserts",
  "description": "Sweet endings",
  "display_order": 5
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 201 | Category created |
| 400 | Validation error |
| 403 | Permission denied |

---

## GET `/menu/items`

Retrieve paginated list of menu items with filtering options.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page` | integer | No | Page number |
| `per_page` | integer | No | Items per page (max 100) |
| `category_id` | integer | No | Filter by category |
| `search` | string | No | Search by name or SKU |
| `available_only` | boolean | No | Only available items |

**Success Response (200):**

```json
{
  "data": [
    {
      "id": 1,
      "name": "Classic Burger",
      "price": 12.99,
      "category_id": 2,
      "sku": "BRG-001",
      "is_available": true,
      "prep_time_minutes": 12
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 45,
    "total_pages": 3
  }
}
```

---

## POST `/menu/items`

Create a new menu item with optional modifiers.

**Authentication Required:** Yes

**Request Body:**

```json
{
  "name": "Bacon Cheeseburger",
  "description": "Half-pound Angus beef with crispy bacon and American cheese",
  "price": 15.99,
  "category_id": 2,
  "sku": "BRG-002",
  "prep_time_minutes": 12,
  "modifier_group_ids": [1, 2]
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 201 | Menu item created |

---

## GET `/menu/items/{id}`

Retrieve detailed menu item information including modifiers and pricing rules.

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Menu item ID |

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `include` | string | No | Include: modifiers, pricing_rules, recipe |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Menu item details |
| 404 | Item not found |

---

## PATCH `/menu/items/{id}/availability`

Quickly mark an item as available or unavailable (86'd).

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Menu item ID |

**Request Body:**

```json
{
  "is_available": false,
  "reason": "Out of buns"
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Availability updated |

---

## GET `/menu/modifier-groups`

Retrieve all modifier groups (e.g., Toppings, Temperature, Sides).

**Authentication Required:** Yes

**Success Response (200):**

```json
{
  "data": [
    {
      "id": 1,
      "name": "Temperature",
      "min_selections": 1,
      "max_selections": 1,
      "is_required": true,
      "modifiers": [
        { "id": 1, "name": "Rare", "price": 0 },
        { "id": 2, "name": "Medium", "price": 0 },
        { "id": 3, "name": "Well Done", "price": 0 }
      ]
    }
  ]
}
```
