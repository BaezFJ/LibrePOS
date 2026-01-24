# Restaurant Point of Sale System

> Product Requirements Document

**Version 1.0 | January 2026**

| Property | Value |
|----------|-------|
| Document Status | Draft - Pending Approval |
| Architecture Pattern | Flask Blueprints with Factory Pattern |
| Total Blueprints | 8 (6 Feature + 2 Supporting) |
| Database | Single PostgreSQL Database |

---

## Executive Summary

This PRD defines the technical architecture and implementation specifications for a comprehensive Restaurant POS system. The system uses Flask's blueprint architecture with a factory pattern, enabling modular development and phased deployment across three priority phases.

The architecture supports both web-based interfaces using Jinja2 templating and a versioned RESTful API for mobile and third-party integrations.

---

## Scope

### In Scope

| Phase | Focus | Blueprints |
|-------|-------|------------|
| **Phase 1** | MVP Core | auth, menu, orders, payments |
| **Phase 2** | Floor Operations | operations, staff |
| **Phase 3** | Analytics | reporting |

**Phase 1: MVP Core**
- Authentication: Login, logout, session management, PIN entry
- Menu Management: Item configuration, categories, modifiers, pricing, combos
- Order Management: Order entry, types, lifecycle, check handling, course management
- Payment Processing: Tender types, tips, adjustments, discounts, taxes, receipts

**Phase 2: Floor Operations**
- Operations: KDS, ticket routing, floor plans, table management, reservations, waitlist
- Staff Management: Users, roles, permissions, time tracking, scheduling

**Phase 3: Analytics**
- Reporting: Sales reports, labor reports, dashboards, audit logs, scheduled reports

### Deferred

| Feature | Strategy |
|---------|----------|
| Inventory | Recipe/cost tracking as menu extensions |
| Customers | Build when loyalty program needed |
| Integrations | Third-party integrations ad-hoc as required |

### Out of Scope

Hardware procurement, payment processor contracts, multi-tenancy support, and native mobile applications are not included in this initial release.

---

## Quick Reference

### Blueprint Structure

Each blueprint is self-contained with:

| Component | Purpose |
|-----------|---------|
| `models.py` | SQLAlchemy model definitions |
| `routes.py` | HTTP route handlers |
| `services.py` | Business logic |
| `schemas.py` | Marshmallow serialization |
| `forms.py` | WTForms definitions |
| `static/` | Blueprint CSS, JS, images |
| `templates/` | Jinja2 templates |

### URL Prefixes

| Blueprint | Web | API |
|-----------|-----|-----|
| auth | `/auth` | `/api/v1/auth` |
| menu | `/menu` | `/api/v1/menu` |
| orders | `/orders` | `/api/v1/orders` |
| payments | `/payments` | `/api/v1/payments` |
| operations | `/operations` | `/api/v1/operations` |
| staff | `/staff` | `/api/v1/staff` |
| reporting | `/reports` | `/api/v1/reports` |

### Core Technology Stack

| Category | Technologies |
|----------|--------------|
| Backend | Flask, SQLAlchemy, Flask-Login, Marshmallow |
| Database | PostgreSQL |
| Frontend | MaterializeCSS, Chart.js, SortableJS, interact.js |
| Security | Flask-Bcrypt, PyJWT |
| Testing | pytest, factory-boy, faker |

---

## Key Commands

```bash
flask run                          # Dev server
flask db migrate -m "msg"          # Generate migration
flask db upgrade                   # Apply migrations
flask pos seed                     # Seed development data
flask pos create-admin             # Create admin user
pytest --cov=app                   # Run tests with coverage
```

---

## Architectural Decisions

| Decision | Choice |
|----------|--------|
| Framework | Flask with factory pattern |
| Blueprints | 8 (6 feature + 2 supporting) |
| Authentication | Flask-Login (web), JWT-ready (API) |
| Database | Single PostgreSQL |
| Frontend | MaterializeCSS + Chart.js, SortableJS, interact.js |
| Model Organization | Blueprint-owned with cross-imports |

---

## Detailed Documentation

- [Architecture](prd/architecture.md) - Design principles, blueprint structure, URL organization
- [Technology Stack](prd/technology-stack.md) - Frameworks, libraries, dependencies
- [Frontend](prd/frontend.md) - MaterializeCSS, Chart.js, SortableJS, interact.js
- [Authentication](prd/authentication.md) - Web auth, API auth, model organization
- [Data Models](prd/data-models.md) - Complete model definitions by blueprint
- [CLI Commands](prd/cli-commands.md) - Application, testing, database commands
- [Implementation Phases](prd/implementation-phases.md) - Phased deployment tiers

---

## Related Documentation

- [Architecture Overview](architecture.md) - System architecture details
- [Database Schema](database-schema.md) - Table definitions and relationships
- [API Documentation](api.md) - RESTful API reference
- [UI/UX Guidelines](uiux.md) - Design system and conventions
- [Components](components.md) - Jinja2 macro library
