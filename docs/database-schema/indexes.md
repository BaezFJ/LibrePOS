# Performance Indexes

> Recommended indexes beyond primary keys and foreign keys (auto-indexed)

---

## Orders & Payments

| Index | Purpose |
|-------|---------|
| `order(status)` | Filter open orders |
| `order(created_at)` | Date range queries |
| `order(server_id, status)` | Server's open orders |
| `order_item(order_id, status)` | Items by order and status |
| `payment(created_at)` | Payment date queries |
| `check(order_id)` | Checks for an order |

---

## Kitchen & Tables

| Index | Purpose |
|-------|---------|
| `kitchen_ticket(station_id, status)` | Station's pending tickets |
| `kitchen_ticket(created_at)` | Ticket timing |
| `table_status(status)` | Find available tables |
| `reservation(reservation_time)` | By date/time |
| `reservation(status)` | Active reservations |

---

## Reporting & Analytics

| Index | Purpose |
|-------|---------|
| `daily_summary(business_date)` | Date lookups |
| `hourly_sales(business_date, hour)` | Hourly breakdown |
| `audit_log(created_at)` | Audit trail |
| `audit_log(user_id, created_at)` | User activity |

---

## Staff & Time

| Index | Purpose |
|-------|---------|
| `user(email)` | Login by email |
| `user(employee_number)` | Lookup by ID |
| `time_entry(user_id, clock_in)` | Employee time records |
| `shift(user_id, scheduled_start)` | Employee schedules |
