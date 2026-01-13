# Static Assets Organization

> Global and blueprint-specific asset structure, frontend libraries.

---

## Global Assets (`app/static/`)

```
app/static/
├── vendor/                       # Third-party libraries
│   ├── bootstrap/
│   │   ├── css/bootstrap.min.css
│   │   └── js/bootstrap.bundle.min.js
│   ├── chartjs/
│   │   └── chart.min.js
│   ├── sortablejs/
│   │   └── Sortable.min.js
│   └── interactjs/
│       └── interact.min.js
│
├── css/
│   ├── main.css                  # Global custom styles
│   ├── variables.css             # CSS custom properties (theme)
│   └── utilities.css             # Utility classes
│
├── js/
│   ├── app.js                    # Global initialization
│   ├── api.js                    # API client utilities
│   └── utils.js                  # Helper functions
│
└── img/
    ├── logo.svg                  # Application logo
    ├── icons/                    # Custom icons
    └── placeholders/             # Placeholder images
```

---

## Blueprint-Specific Assets

```
app/blueprints/kitchen/static/
├── css/
│   └── kds.css                   # KDS-specific styles
└── js/
    ├── kds.js                    # KDS functionality
    └── ticket-manager.js         # Ticket operations

app/blueprints/tables/static/
├── css/
│   └── floor-plan.css            # Floor plan editor styles
└── js/
    ├── floor-editor.js           # interact.js floor plan editor
    └── reservation-calendar.js   # Reservation management
```

---

## Frontend Libraries

| Library | Version | Purpose | Location |
|---------|---------|---------|----------|
| Bootstrap | 5.3.8 | UI framework, components | `vendor/bootstrap/` |
| Chart.js | 4.x | Dashboard charts | `vendor/chartjs/` |
| SortableJS | 1.15.x | Drag-drop reordering | `vendor/sortablejs/` |
| interact.js | 1.10.x | Floor plan editor | `vendor/interactjs/` |
