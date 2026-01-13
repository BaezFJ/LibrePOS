# POS System API Documentation

> RESTful API for the Restaurant Point of Sale System

**Version:** 1.0.0 | **Base URL:** `/api/v1`

---

## Overview

Complete API enabling integration with ordering, payments, inventory, staff management, and more.

### Base URLs

| Environment | URL |
|-------------|-----|
| Production | `https://api.restaurant-pos.com/api/v1` |
| Staging | `https://staging-api.restaurant-pos.com/api/v1` |
| Local | `http://localhost:5000/api/v1` |

---

## API Conventions

### Authentication

| Method | Use Case |
|--------|----------|
| Session Auth | Web clients (Flask-Login) |
| Bearer Token | JWT for API clients |
| API Key | Third-party integrations |

### Rate Limiting

| Endpoint Type | Limit |
|---------------|-------|
| Standard | 100/min |
| Search | 30/min |
| Batch | 10/min |

### Pagination

| Parameter | Description |
|-----------|-------------|
| `page` | Page number (default: 1) |
| `per_page` | Items per page (default: 20, max: 100) |

### Error Format

```json
{
  "error": "error_code",
  "message": "Human-readable message",
  "details": {}
}
```

---

## Endpoint Summary

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
| PATCH | `/menu/items/{id}/availability` | Toggle availability (86) |
| GET | `/menu/modifier-groups` | List modifier groups |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/orders` | List orders |
| POST | `/orders` | Create new order |
| GET | `/orders/{id}` | Get order by ID |
| POST | `/orders/{id}/items` | Add item to order |
| POST | `/orders/{id}/submit` | Submit to kitchen |
| POST | `/orders/{id}/void` | Void entire order |
| POST | `/orders/{id}/checks` | Create/split check |

### Payments
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/payments/process` | Process payment |
| POST | `/payments/{id}/void` | Void payment |
| POST | `/payments/{id}/refund` | Refund payment |
| POST | `/payments/{id}/tip` | Add/adjust tip |
| POST | `/checks/{id}/discount` | Apply discount |
| GET | `/discounts` | List discounts |
| POST | `/cash-drawers/{id}/open` | Open drawer |
| POST | `/cash-drawers/{id}/close` | Close drawer |

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
| POST | `/kitchen/tickets/{id}/start` | Start ticket |
| POST | `/kitchen/tickets/{id}/bump` | Bump ticket |
| GET | `/kitchen/all-day` | Get all-day counts |
| GET | `/kitchen/stations` | List stations |

### Tables
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tables/floor-plans/{id}` | Get floor plan |
| GET | `/tables` | List tables |
| POST | `/tables/{id}/seat` | Seat party |
| PATCH | `/tables/{id}/status` | Update status |
| GET | `/reservations` | List reservations |
| POST | `/reservations` | Create reservation |
| GET | `/waitlist` | Get waitlist |
| POST | `/waitlist/{id}/notify` | Notify party |

### Reporting
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/reports/daily-summary` | Daily summary |
| GET | `/reports/sales` | Sales report |
| GET | `/reports/product-mix` | Product mix |
| GET | `/reports/labor` | Labor report |
| GET | `/reports/audit-log` | Audit log |

### Inventory
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory/items` | List items |
| POST | `/inventory/items/{id}/adjust` | Adjust stock |
| GET | `/inventory/vendors` | List vendors |
| POST | `/inventory/purchase-orders` | Create PO |
| POST | `/inventory/purchase-orders/{id}/receive` | Receive items |

### Customers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/customers` | List customers |
| GET | `/customers/lookup` | Lookup customer |
| GET | `/loyalty/accounts/{id}` | Get loyalty account |
| POST | `/loyalty/redeem` | Redeem reward |
| GET | `/gift-cards/{card_number}` | Check balance |
| POST | `/gift-cards/{card_number}/redeem` | Redeem card |

### Integrations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/integrations` | List integrations |
| POST | `/integrations/{id}/sync` | Trigger sync |
| GET | `/external-orders` | List external orders |
| POST | `/external-orders/{id}/accept` | Accept order |
| POST | `/webhooks` | Create webhook |

---

## Detailed Documentation

- [Authentication](api/auth.md) - Login, logout, tokens, user profile
- [Menu](api/menu.md) - Categories, items, modifiers, availability
- [Orders](api/orders.md) - Order lifecycle, items, checks
- [Payments](api/payments.md) - Processing, voids, refunds, discounts, cash drawers
- [Staff](api/staff.md) - Employees, roles, time tracking
- [Kitchen](api/kitchen.md) - KDS, tickets, stations, all-day counts
- [Tables](api/tables.md) - Floor plans, reservations, waitlist
- [Reporting](api/reporting.md) - Sales, labor, product mix, audit log
- [Inventory](api/inventory.md) - Stock, vendors, purchase orders
- [Customers](api/customers.md) - Profiles, loyalty, gift cards
- [Integrations](api/integrations.md) - Third-party, webhooks, external orders
