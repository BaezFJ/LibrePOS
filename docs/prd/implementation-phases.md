# Implementation Phases

> Phased deployment across three priority phases optimized for solo development

---

## Phase 1: MVP Core

Minimum viable POS functionality enabling basic restaurant operations.

| Blueprint | Deliverables |
|-----------|--------------|
| auth | Login, logout, session management, PIN entry |
| menu | Item CRUD, categories, modifiers, pricing rules |
| orders | Order entry, modification, status tracking, check handling |
| payments | Payment processing, tips, discounts, receipts |

---

## Phase 2: Floor Operations

Features required for efficient daily restaurant operations.

| Blueprint | Deliverables |
|-----------|--------------|
| operations | KDS interface, ticket routing, floor plans, table management, reservations, waitlist |
| staff | User management, roles, permissions, time tracking, scheduling |

---

## Phase 3: Analytics

Business insights and reporting for optimization.

| Blueprint | Deliverables |
|-----------|--------------|
| reporting | Sales reports, labor reports, dashboards, audit logs, scheduled reports |

---

## Deferred Features

The following features are deferred for later implementation when specific needs arise:

| Feature | Strategy | Notes |
|---------|----------|-------|
| **Inventory** | Menu extensions | Recipe/cost tracking as menu features |
| **Customers** | Future blueprint | Build when loyalty program needed |
| **Integrations** | Ad-hoc | Third-party integrations as required |

---

## Summary of Architectural Decisions

| Decision Area | Choice |
|---------------|--------|
| Framework | Flask with factory pattern |
| Blueprint Count | 8 (6 feature + 2 supporting) |
| Blueprint Structure | Self-contained with own `static/` and `templates/` |
| API Strategy | Separate versioned api blueprint (`/api/v1/...`) |
| Template Engine | Jinja2 with extensions |
| Web Authentication | Flask-Login (session-based) |
| API Authentication | JWT-ready architecture (session initially) |
| Model Organization | Blueprint-owned with cross-imports |
| Database | Single PostgreSQL database |
| CLI Tools | Flask CLI commands with click |
| Frontend Styling | MaterializeCSS with Chart.js, SortableJS, interact.js |
