# Dropdown Component

> Dropdown menus for actions, navigation, and app grids.

```jinja
{% import "components/_dropdown.html" as Dropdown %}
```

---

## Macros

| Macro | Parameters | Description |
|-------|------------|-------------|
| `render(id, class_)` | `id`, `class_=''` | Dropdown container (use with `{% call %}`) |
| `trigger(id, icon, label, class_)` | `id`, `icon='more_vert'`, `label=None`, `class_=''` | Trigger button |
| `item(label, url, icon, badge, disabled, active, class_)` | See below | Menu item |
| `header(text, class_)` | `text`, `class_=''` | Section header |
| `tile(icon, label, url, class_)` | `icon`, `label=None`, `url='#'`, `class_=''` | App grid tile |
| `divider()` | - | Horizontal divider |

---

## `item()` Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | str | - | Menu item text |
| `url` | str | `'#'` | Destination URL |
| `icon` | str | `None` | Material Symbols icon |
| `badge` | int | `None` | Notification count |
| `disabled` | bool | `False` | Disabled state |
| `active` | bool | `False` | Active/selected state |
| `class_` | str | `''` | Additional CSS classes |

---

## Examples

### Basic Dropdown

```jinja
{{ Dropdown.trigger("actions-menu") }}

{% call Dropdown.render("actions-menu") %}
    {{ Dropdown.item("Edit", url_for('menu.edit', id=item.id), icon="edit") }}
    {{ Dropdown.item("Duplicate", url_for('menu.duplicate', id=item.id), icon="content_copy") }}
    {{ Dropdown.divider() }}
    {{ Dropdown.item("Delete", url_for('menu.delete', id=item.id), icon="delete", class_="red-text") }}
{% endcall %}
```

### With Sections

```jinja
{{ Dropdown.trigger("user-menu", icon="person", label="Account") }}

{% call Dropdown.render("user-menu") %}
    {{ Dropdown.header("Account") }}
    {{ Dropdown.item("Profile", url_for('staff.profile'), icon="person") }}
    {{ Dropdown.item("Settings", url_for('staff.settings'), icon="settings") }}
    {{ Dropdown.divider() }}
    {{ Dropdown.header("Notifications") }}
    {{ Dropdown.item("Messages", url_for('staff.messages'), icon="mail", badge=3) }}
    {{ Dropdown.divider() }}
    {{ Dropdown.item("Logout", url_for('auth.logout'), icon="logout", class_="red-text") }}
{% endcall %}
```

### Item States

```jinja
{{ Dropdown.item("Current Page", "#", active=True) }}
{{ Dropdown.item("Unavailable", "#", disabled=True) }}
```

### Apps Grid

```jinja
{% call Dropdown.render("apps-dropdown", class_="apps-dropdown") %}
    {{ Dropdown.tile("point_of_sale", "POS", url_for('orders.pos')) }}
    {{ Dropdown.tile("restaurant_menu", "Menu", url_for('menu.index')) }}
    {{ Dropdown.tile("groups", "Staff", url_for('staff.index')) }}
{% endcall %}
```
