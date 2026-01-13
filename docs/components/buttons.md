# Button Component

> Bootstrap button components with support for links and action buttons.

```jinja
{% import "macros/button.html" as Button %}
```

---

## Button Types

| Type | Description |
|------|-------------|
| `filled` | Primary actions (solid background) - default |
| `tonal` | Secondary actions (tonal background) |
| `outlined` | Bordered with transparent background |
| `elevated` | Raised with shadow |
| `text` | Text-only, no background |

---

## Base Macros

| Macro | Element | Description |
|-------|---------|-------------|
| `render(text, url, type, icon, ...)` | `<a>` | Link button for navigation |
| `button(text, type, button_type, icon, ...)` | `<button>` | Action button for forms |

### Common Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | str | - | Button label text |
| `icon` | str | `None` | Material Symbols icon name |
| `icon_position` | str | `'left'` | Icon position: 'left' or 'right' |
| `hide_text_mobile` | bool | `False` | Hide text on small screens |
| `class_` | str | `''` | Additional CSS classes |

**Link-specific:** `url` (str, default `'#'`)

**Button-specific:** `button_type` (str: 'button', 'submit', 'reset'), `disabled` (bool)

---

## Semantic Link Macros (`<a>`)

| Macro | Type | Usage |
|-------|------|-------|
| `filled(text, url, icon, ...)` | filled | Primary action links |
| `tonal(text, url, icon, ...)` | tonal | Secondary action links |
| `outlined(text, url, icon, ...)` | outlined | Bordered links |
| `elevated(text, url, icon, ...)` | elevated | Raised links |
| `text_link(text, url, icon, ...)` | text | Text-only links |

---

## Semantic Button Macros (`<button>`)

| Macro | Type | Usage |
|-------|------|-------|
| `filled_btn(text, icon, ...)` | filled | Primary action buttons |
| `tonal_btn(text, icon, ...)` | tonal | Secondary action buttons |
| `outlined_btn(text, icon, ...)` | outlined | Bordered buttons |
| `elevated_btn(text, icon, ...)` | elevated | Raised buttons |
| `text_btn(text, icon, ...)` | text | Text-only buttons |
| `submit(text, icon, ...)` | filled | Form submit buttons |

---

## Examples

### Link Buttons

```jinja
{# Primary action #}
{{ Button.filled("Save", url="/save", icon="save") }}

{# Secondary action #}
{{ Button.outlined("Cancel", url="/cancel") }}

{# With icon on right #}
{{ Button.tonal("Next", url="/next", icon="arrow_forward", icon_position="right") }}

{# Icon-only on mobile #}
{{ Button.filled("Dashboard", url="/", icon="home", hide_text_mobile=True) }}
```

### Action Buttons

```jinja
{# Form submit #}
{{ Button.submit("Create Account", icon="person_add") }}

{# Generic button #}
{{ Button.filled_btn("Save", icon="save") }}

{# Disabled state #}
{{ Button.filled_btn("Processing...", disabled=True) }}

{# Destructive action #}
{{ Button.outlined_btn("Delete", icon="delete", class_="red-text") }}
```

### Using Base Macros

```jinja
{# Full control with render() #}
{{ Button.render("Custom", url="/page", type="elevated", icon="star", class_="pulse") }}

{# Full control with button() #}
{{ Button.button("Reset", type="outlined", button_type="reset", icon="refresh") }}
```
