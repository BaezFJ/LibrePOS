# Template Organization

> Jinja2 template structure, layouts, macros, and configuration.

---

## Base Templates (`app/templates/`)

```
app/templates/
├── base.html                     # Master template
│   ├── <!DOCTYPE html>
│   ├── <head> meta, CSS links
│   ├── {% block content %}
│   └── <scripts> JS includes
│
├── layouts/
│   ├── admin.html                # Back-office layout (sidebar nav)
│   ├── pos.html                  # POS terminal layout (full-screen)
│   └── kds.html                  # Kitchen display (no nav, auto-refresh)
│
├── macros/
│   ├── forms.html                # {{ form_field(field) }}
│   ├── cards.html                # {{ menu_item_card(item) }}
│   ├── badges.html               # {{ status_badge(status) }}
│   └── modals.html               # {{ confirm_modal(id, title) }}
│
├── components/
│   ├── _navbar.html              # Navigation bar partial
│   ├── _sidebar.html             # Admin sidebar partial
│   ├── _pagination.html          # Pagination controls
│   └── _flash_messages.html      # Alert messages
│
└── errors/
    ├── 404.html                  # Not found
    ├── 403.html                  # Forbidden
    └── 500.html                  # Server error
```

---

## Blueprint Templates

```
app/blueprints/orders/templates/orders/
├── index.html                    # Order list view
├── detail.html                   # Single order view
├── entry.html                    # Order entry screen
├── checkout.html                 # Payment/checkout screen
└── partials/
    ├── _order_item.html          # Order item row
    ├── _order_totals.html        # Order totals display
    └── _modifier_selector.html   # Modifier selection modal
```

---

## Jinja2 Configuration

### Extensions

- `jinja2.ext.do` - Execute statements in templates
- `jinja2.ext.loopcontrols` - Break/continue in loops
- `jinja2.ext.debug` - Debug output (development only)

### Custom Filters

| Filter | Purpose | Example |
|--------|---------|---------|
| `currency` | Format money | `{{ 12.50 \| currency }}` → `$12.50` |
| `timeago` | Relative time | `{{ created_at \| timeago }}` → `5 min ago` |
| `pluralize` | Smart plural | `{{ count \| pluralize('item') }}` |
| `status_badge` | Status HTML | `{{ 'completed' \| status_badge }}` |

### Context Processors

| Variable | Purpose |
|----------|---------|
| `current_location` | Active restaurant location |
| `current_shift` | Active shift for logged-in staff |
| `permissions` | User permission set for UI conditionals |
