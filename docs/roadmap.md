# LibrePOS Feature Roadmap

This document outlines the planned features for LibrePOS, organized by development phase. Features are prioritized to build a solid foundation before adding advanced capabilities.

## Legend

| Status | Meaning |
|--------|---------|
| :white_check_mark: | Completed |
| :construction: | In Progress |
| :white_large_square: | Planned |

---

## Phase 1: Foundation (Core Infrastructure)

Essential infrastructure that other features depend on.

| Status | Feature | Description |
|--------|---------|-------------|
| :white_check_mark: | User Authentication | Secure login/logout with session management |
| :white_check_mark: | Role-Based Access Control | Granular permissions based on user roles (owner, admin, manager, cashier) |
| :white_check_mark: | User Management | Create, edit, and manage user accounts |
| :white_check_mark: | Staff Profiles | Employee directory with contact information |
| :white_large_square: | Business Settings | Configure business name, address, tax rates, currency |
| :white_large_square: | Multi-Location Support | Manage multiple restaurant locations from one system |

---

## Phase 2: Core POS Operations

The fundamental features needed to run daily operations.

### Menu & Products

| Status | Feature | Description |
|--------|---------|-------------|
| :white_large_square: | Menu Categories | Organize items into categories (appetizers, mains, desserts, drinks) |
| :white_large_square: | Menu Items | Add products with name, price, description, and image |
| :white_large_square: | Item Modifiers | Options and add-ons (size, toppings, preparation style) |
| :white_large_square: | Item Availability | Mark items as available, sold out, or hidden |

### Order Management

| Status | Feature | Description |
|--------|---------|-------------|
| :white_large_square: | New Order | Create orders for dine-in, takeout, or delivery |
| :white_large_square: | Order Editing | Modify items, quantities, and special instructions |
| :white_large_square: | Order Status Tracking | Track orders through placed → preparing → ready → completed |
| :white_large_square: | Special Requests | Add notes for dietary restrictions or preparation preferences |

### Payments

| Status | Feature | Description |
|--------|---------|-------------|
| :white_large_square: | Cash Payments | Process cash transactions with change calculation |
| :white_large_square: | Card Payments | Accept credit/debit cards (integration-ready) |
| :white_large_square: | Split Bills | Divide payment between multiple customers |
| :white_large_square: | Tips | Add and track gratuities |
| :white_large_square: | Receipts | Generate and print/email receipts |

### Table Management

| Status | Feature | Description |
|--------|---------|-------------|
| :white_large_square: | Floor Plan | Visual layout of tables and seating areas |
| :white_large_square: | Table Status | Track available, occupied, reserved tables |
| :white_large_square: | Table Assignment | Assign orders to specific tables |
| :white_large_square: | Merge/Transfer Tables | Combine or move orders between tables |

---

## Phase 3: Kitchen & Operations

Features that improve kitchen efficiency and back-of-house operations.

### Kitchen Display System (KDS)

| Status | Feature | Description |
|--------|---------|-------------|
| :white_large_square: | Order Queue | Display incoming orders for kitchen staff |
| :white_large_square: | Order Prioritization | Highlight rush orders or sort by type |
| :white_large_square: | Order Completion | Mark items/orders as prepared |
| :white_large_square: | Modification Alerts | Highlight order changes or special requests |

### Inventory

| Status | Feature | Description |
|--------|---------|-------------|
| :white_large_square: | Stock Tracking | Monitor inventory levels in real time |
| :white_large_square: | Low Stock Alerts | Notifications when items fall below threshold |
| :white_large_square: | Ingredient Management | Track ingredients used in menu items |
| :white_large_square: | Stock Adjustments | Record waste, spillage, or manual corrections |

---

## Phase 4: Reporting & Analytics

Data-driven insights for business decisions.

| Status | Feature | Description |
|--------|---------|-------------|
| :white_large_square: | Sales Reports | Daily, weekly, monthly revenue summaries |
| :white_large_square: | Product Performance | Best sellers, slow movers, category breakdown |
| :white_large_square: | Employee Reports | Sales by staff member, hours worked |
| :white_large_square: | Tax Reports | Sales tax calculations for accounting |
| :white_large_square: | Inventory Reports | Stock levels, usage trends, waste tracking |
| :white_large_square: | Export Data | Download reports as CSV/PDF |

---

## Phase 5: Customer Experience

Features that enhance the customer-facing experience.

### Customer Management

| Status | Feature | Description |
|--------|---------|-------------|
| :white_large_square: | Customer Profiles | Store contact info and preferences |
| :white_large_square: | Order History | View past orders for quick reordering |
| :white_large_square: | Dietary Notes | Track allergies and dietary restrictions |

### Loyalty & Promotions

| Status | Feature | Description |
|--------|---------|-------------|
| :white_large_square: | Discounts | Percentage or fixed-amount discounts |
| :white_large_square: | Happy Hour Pricing | Time-based automatic price adjustments |
| :white_large_square: | Loyalty Points | Reward repeat customers |
| :white_large_square: | Promotional Codes | Single-use or campaign discount codes |

### Reservations

| Status | Feature | Description |
|--------|---------|-------------|
| :white_large_square: | Reservation Calendar | Accept and manage table reservations |
| :white_large_square: | Waitlist | Manage walk-in queues during busy periods |
| :white_large_square: | Confirmation Notifications | Email/SMS reservation confirmations |

---

## Phase 6: Integrations & Hardware

Connecting LibrePOS to external systems and devices.

### Hardware Support

| Status | Feature | Description |
|--------|---------|-------------|
| :white_large_square: | Receipt Printers | Thermal printer support for receipts and kitchen tickets |
| :white_large_square: | Cash Drawers | Automatic drawer open on cash transactions |
| :white_large_square: | Barcode Scanners | Scan packaged items for quick entry |
| :white_large_square: | Card Readers | EMV/NFC payment terminal integration |

### External Integrations

| Status | Feature | Description |
|--------|---------|-------------|
| :white_large_square: | Accounting Export | Integration with QuickBooks, Xero, etc. |
| :white_large_square: | Delivery Platforms | Sync with DoorDash, UberEats, etc. |
| :white_large_square: | Online Ordering | Customer-facing order website |

---

## Future Considerations

Advanced features for future exploration:

- **QR Code Ordering** - Contactless ordering from customer devices
- **Voice Ordering** - Voice command input for hands-free operation
- **Multi-Language Receipts** - Customer-selected language for receipts
- **Dynamic Pricing** - Demand-based price adjustments
- **Predictive Analytics** - AI-powered sales forecasting
- **Vendor Management** - Automated reordering from suppliers

---

## Contributing

Want to help build a feature? Check the [contributing guidelines](../README.md#contributing) and open an issue to discuss implementation before starting work.