# POS System API Documentation

**Version 1.0.0**

**Base URL:** `/api/v1`

---

## Overview

Complete RESTful API documentation for the Restaurant Point of Sale System. This API enables integration with ordering, payments, inventory, staff management, and more.

### Base URLs

| Environment | URL |
|-------------|-----|
| Production | `https://api.restaurant-pos.com/api/v1` |
| Staging | `https://staging-api.restaurant-pos.com/api/v1` |
| Local | `http://localhost:5000/api/v1` |

---

## API Conventions

### Authentication

The API supports multiple authentication methods:

- **Session Auth** - For web clients (Flask-Login)
- **Bearer Token** - JWT for API clients
- **API Key** - For third-party integrations

### Rate Limiting

Requests are rate limited per authentication context:

| Endpoint Type | Limit |
|---------------|-------|
| Standard endpoints | 100/min |
| Search endpoints | 30/min |
| Batch operations | 10/min |

### Pagination

List endpoints support pagination with query parameters:

| Parameter | Description |
|-----------|-------------|
| `page` | Page number (default: 1) |
| `per_page` | Items per page (default: 20, max: 100) |

### Error Handling

All errors return a consistent JSON format:

```json
{
  "error": "error_code",
  "message": "Human-readable message",
  "details": {}
}
```

---

## 1. Authentication

Endpoints for user authentication, session management, and token handling.

### POST `/auth/login`

Authenticate user with PIN or password credentials. Returns access token and user details.

**Authentication Required:** No

**Request Body:**

```json
{
  "employee_number": "EMP001",
  "pin": "1234"
}
```

Or password-based:

```json
{
  "email": "manager@restaurant.com",
  "password": "securepassword"
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Login successful |
| 401 | Invalid credentials |
| 429 | Too many login attempts |

**Success Response (200):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "role": "Server"
  }
}
```

---

### POST `/auth/logout`

Invalidate the current session and access token.

**Authentication Required:** Yes

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Logout successful |

**Success Response (200):**

```json
{
  "message": "Successfully logged out"
}
```

---

### POST `/auth/refresh`

Exchange a valid refresh token for a new access token.

**Authentication Required:** No

**Request Body:**

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Token refreshed |
| 401 | Invalid refresh token |

---

### GET `/auth/me`

Retrieve the profile and permissions of the currently authenticated user.

**Authentication Required:** Yes

**Success Response (200):**

```json
{
  "id": 1,
  "employee_number": "EMP001",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@restaurant.com",
  "role": {
    "id": 3,
    "name": "Server",
    "permissions": ["create_order", "process_payment"]
  }
}
```

---

## 2. Menu

Manage menu items, categories, modifiers, pricing rules, and availability.

### GET `/menu/categories`

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

### POST `/menu/categories`

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

### GET `/menu/items`

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

### POST `/menu/items`

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

### GET `/menu/items/{id}`

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

### PATCH `/menu/items/{id}/availability`

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

### GET `/menu/modifier-groups`

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

---

## 3. Orders

Create and manage orders, order items, and checks.

### GET `/orders`

Retrieve paginated list of orders with filtering options.

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | Filter by status: draft, submitted, preparing, ready, completed, cancelled |
| `order_type` | string | No | Filter by type: dine_in, takeout, delivery, bar |
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

### POST `/orders`

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

### GET `/orders/{id}`

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

### POST `/orders/{id}/items`

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

### POST `/orders/{id}/submit`

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

### POST `/orders/{id}/void`

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

### POST `/orders/{id}/checks`

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

---

## 4. Payments

Process payments, manage tips, discounts, and cash drawers.

### POST `/payments/process`

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

### POST `/payments/{id}/void`

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

### POST `/payments/{id}/refund`

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

### POST `/payments/{id}/tip`

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

### POST `/checks/{id}/discount`

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

### GET `/discounts`

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

### POST `/cash-drawers/{id}/open`

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

### POST `/cash-drawers/{id}/close`

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

---

## 5. Staff

Manage employees, roles, permissions, time tracking, and scheduling.

### GET `/staff/users`

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

### POST `/staff/users`

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

### POST `/staff/clock-in`

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

### POST `/staff/clock-out`

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

### GET `/staff/roles`

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

### GET `/staff/time-entries`

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

---

## 6. Kitchen

Kitchen display system, ticket management, and station operations.

### GET `/kitchen/tickets`

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

### POST `/kitchen/tickets/{id}/start`

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

### POST `/kitchen/tickets/{id}/bump`

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

### GET `/kitchen/all-day`

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

### GET `/kitchen/stations`

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

---

## 7. Tables

Floor plans, table management, reservations, and waitlist.

### GET `/tables/floor-plans/{id}`

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

### GET `/tables`

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

### POST `/tables/{id}/seat`

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

### PATCH `/tables/{id}/status`

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

### GET `/reservations`

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

### POST `/reservations`

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

### GET `/waitlist`

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

### POST `/waitlist/{id}/notify`

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

---

## 8. Reporting

Sales reports, analytics, labor reports, and audit logs.

### GET `/reports/daily-summary`

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

### GET `/reports/sales`

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

### GET `/reports/product-mix`

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

### GET `/reports/labor`

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

### GET `/reports/audit-log`

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

---

## 9. Inventory

Stock management, recipes, vendors, and purchase orders.

### GET `/inventory/items`

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

### POST `/inventory/items/{id}/adjust`

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

### GET `/inventory/vendors`

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

### POST `/inventory/purchase-orders`

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

### POST `/inventory/purchase-orders/{id}/receive`

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

---

## 10. Customers

Customer profiles, loyalty program, gift cards, and feedback.

### GET `/customers`

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

### GET `/customers/lookup`

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

### GET `/loyalty/accounts/{id}`

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

### POST `/loyalty/redeem`

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

### GET `/gift-cards/{card_number}`

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

### POST `/gift-cards/{card_number}/redeem`

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

---

## 11. Integrations

Third-party integrations, webhooks, and external orders.

### GET `/integrations`

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

### POST `/integrations/{id}/sync`

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

### GET `/external-orders`

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

### POST `/external-orders/{id}/accept`

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

### POST `/webhooks`

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

---

## Appendix: API Endpoint Summary

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Authenticate user |
| POST | `/auth/logout` | End session |
| POST | `/auth/refresh` | Refresh access token |
| GET | `/auth/me` | Get current user info |

### Menu
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/menu/categories` | List all categories |
| POST | `/menu/categories` | Create category |
| GET | `/menu/items` | List menu items |
| POST | `/menu/items` | Create menu item |
| GET | `/menu/items/{id}` | Get menu item by ID |
| PATCH | `/menu/items/{id}/availability` | Toggle item availability (86) |
| GET | `/menu/modifier-groups` | List modifier groups |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/orders` | List orders |
| POST | `/orders` | Create new order |
| GET | `/orders/{id}` | Get order by ID |
| POST | `/orders/{id}/items` | Add item to order |
| POST | `/orders/{id}/submit` | Submit order to kitchen |
| POST | `/orders/{id}/void` | Void entire order |
| POST | `/orders/{id}/checks` | Create/split check |

### Payments
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

### Staff
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/staff/users` | List employees |
| POST | `/staff/users` | Create employee |
| POST | `/staff/clock-in` | Clock in |
| POST | `/staff/clock-out` | Clock out |
| GET | `/staff/roles` | List roles |
| GET | `/staff/time-entries` | List time entries |

### Kitchen
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/kitchen/tickets` | List kitchen tickets |
| POST | `/kitchen/tickets/{id}/start` | Start cooking ticket |
| POST | `/kitchen/tickets/{id}/bump` | Bump/complete ticket |
| GET | `/kitchen/all-day` | Get all-day counts |
| GET | `/kitchen/stations` | List kitchen stations |

### Tables
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

### Reporting
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/reports/daily-summary` | Get daily summary |
| GET | `/reports/sales` | Get sales report |
| GET | `/reports/product-mix` | Get product mix report |
| GET | `/reports/labor` | Get labor report |
| GET | `/reports/audit-log` | Get audit log |

### Inventory
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory/items` | List inventory items |
| POST | `/inventory/items/{id}/adjust` | Adjust stock level |
| GET | `/inventory/vendors` | List vendors |
| POST | `/inventory/purchase-orders` | Create purchase order |
| POST | `/inventory/purchase-orders/{id}/receive` | Receive items from PO |

### Customers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/customers` | List customers |
| GET | `/customers/lookup` | Lookup customer |
| GET | `/loyalty/accounts/{id}` | Get loyalty account |
| POST | `/loyalty/redeem` | Redeem reward |
| GET | `/gift-cards/{card_number}` | Check gift card balance |
| POST | `/gift-cards/{card_number}/redeem` | Redeem gift card |

### Integrations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/integrations` | List integrations |
| POST | `/integrations/{id}/sync` | Trigger manual sync |
| GET | `/external-orders` | List external orders |
| POST | `/external-orders/{id}/accept` | Accept external order |
| POST | `/webhooks` | Create webhook endpoint |

---

*End of API Documentation*
