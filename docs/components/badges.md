# Badge Component

> MaterializeCSS badge components for status indicators and notifications.

```jinja
{% import "macros/badge.html" as Badge %}
```

---

## Base Macro

| Macro | Parameters | Description |
|-------|------------|-------------|
| `render(data, caption, new, color, class_)` | `data`, `caption=None`, `new=False`, `color=None`, `class_=''` | Renders badge element |

---

## Semantic Badge Macros

### Status Badges

For order/item status indicators.

| Macro | Color | Usage |
|-------|-------|-------|
| `pending(text, class_)` | orange | Awaiting action |
| `in_progress(text, class_)` | blue | Being processed |
| `completed(text, class_)` | green | Successfully done |
| `cancelled(text, class_)` | red | Cancelled/failed |

### Color Variants

| Macro | Color | Usage |
|-------|-------|-------|
| `success(data, caption, class_)` | green | Success states |
| `warning(data, caption, class_)` | orange | Warning states |
| `error(data, caption, class_)` | red | Error states |
| `info(data, caption, class_)` | blue | Informational |

### Notification Badges

| Macro | Description |
|-------|-------------|
| `count(number, caption, class_)` | Notification count (cart items, unread) |
| `notification(text, caption, color, class_)` | Generic notification with 'new' styling |

---

## Examples

```jinja
{# Status badges #}
{{ Badge.pending() }}
{{ Badge.completed() }}
{{ Badge.cancelled("Refunded") }}

{# Color variants #}
{{ Badge.success("Active") }}
{{ Badge.error("Offline") }}
{{ Badge.warning("Low Stock", caption="items") }}

{# Notification counts #}
{{ Badge.count(5) }}
{{ Badge.count(3, caption="items") }}

{# Generic with options #}
{{ Badge.render("Sale", color="red") }}
{{ Badge.render("99+", new=True, color="blue") }}
```
