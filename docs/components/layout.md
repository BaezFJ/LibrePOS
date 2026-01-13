# Layout Components

> Page structure elements: Navbar, Sidebar, Footer

---

## Navbar (`components/_navbar.html`)

Top navigation bar with support for dropdowns and mobile triggers.

```jinja
{% import "components/_navbar.html" as Navbar %}
```

### Macros

| Macro | Parameters | Description |
|-------|------------|-------------|
| `render()` | - | Container wrapper (use with `{% call %}`) |
| `title(text)` | `text` | Centered brand title |
| `item(label, icon, url, dynamic)` | `label`, `icon`, `url`, `dynamic=True` | Nav item link |
| `dropdown_trigger(label, icon, target)` | `label`, `icon`, `target` | Dropdown trigger button |
| `dropdown(label, icon, target, class_)` | `label`, `icon`, `target`, `class_` | Full dropdown with trigger |
| `dropdown_item(label, icon, url)` | `label`, `icon`, `url` | Item inside dropdown |
| `sidenav_trigger(target)` | `target="mainMenu"` | Mobile sidenav toggle |

### Example

```jinja
{% call Navbar.render() %}
    <ul class="left">
        {{ Navbar.sidenav_trigger() }}
    </ul>
    {{ Navbar.title("Menu Management") }}
    <ul class="right">
        {{ Navbar.item("Dashboard", "dashboard", url_for('main.dashboard')) }}
        {% call Navbar.dropdown("Settings", "settings", "settings-dropdown") %}
            {{ Navbar.dropdown_item("Profile", "person", url_for('staff.profile')) }}
            {{ Navbar.dropdown_item("Logout", "logout", url_for('auth.logout')) }}
        {% endcall %}
    </ul>
{% endcall %}
```

---

## Sidebar (`components/_sidebar.html`)

Fixed side navigation with collapsible sections.

```jinja
{% import "components/_sidebar.html" as Sidebar with context %}
```

### Macros

| Macro | Parameters | Description |
|-------|------------|-------------|
| `render(title, id)` | `title`, `id="mainMenu"` | Sidenav container (use with `{% call %}`) |
| `item(label, icon, url, active)` | `label`, `icon`, `url`, `active=False` | Nav item (auto-detects active state) |
| `collapsible(text, icon)` | `text`, `icon` | Collapsible section (use with `{% call %}`) |
| `divider()` | - | Horizontal divider |
| `subheader(label)` | `label` | Section subheader |

### `render(title, id)`

Container macro that wraps all sidebar content. Must be used with Jinja2's `{% call %}` block.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | - | Unused (uses `sidenav_title` context variable instead) |
| `id` | string | `"mainMenu"` | HTML id attribute for the sidebar |

**Context Variables:**
- `sidenav_title` - Brand text displayed in header (defaults to "LibrePOS")
- `app_version` - If defined, displays version in footer

### `item(label, icon, url, active)`

Creates a single navigation link item.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | string | - | Display text for the link |
| `icon` | string | - | Material Icons icon name |
| `url` | string | `""` | Destination URL |
| `active` | bool | `False` | Force active state (auto-detected from `request.path`) |

```jinja
{{ Sidebar.item("Dashboard", url=url_for('menu.index'), icon="dashboard") }}
{{ Sidebar.item("Settings", url="/settings", icon="settings", active=True) }}
```

### `subheader(label)`

Creates a non-clickable section header to group related items.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | string | - | Section title text |

```jinja
{{ Sidebar.subheader("Configuration") }}
{{ Sidebar.item("Settings", url="/settings", icon="settings") }}
```

### `collapsible(text, icon)`

Creates an expandable accordion section. Must be used with `{% call %}` to nest child items.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | - | Header text for the collapsible |
| `icon` | string | - | Material Icons icon name |

```jinja
{% call Sidebar.collapsible("Reports", icon="analytics") %}
    {{ Sidebar.item("Sales", url="/reports/sales") }}
    {{ Sidebar.item("Inventory", url="/reports/inventory") }}
{% endcall %}
```

### `divider()`

Renders a horizontal line separator between navigation sections. Takes no parameters.

```jinja
{{ Sidebar.item("Dashboard", url="/", icon="dashboard") }}
{{ Sidebar.divider() }}
{{ Sidebar.item("Logout", url="/auth/logout", icon="logout") }}
```

### Complete Example

```jinja
{% import "components/_sidebar.html" as Sidebar with context %}

{% call Sidebar.render() %}
    {{ Sidebar.item("Dashboard", url=url_for('menu.index'), icon="dashboard") }}

    {{ Sidebar.subheader("Catalog") }}
    {{ Sidebar.item("Menu Items", url=url_for('menu.items'), icon="restaurant_menu") }}
    {{ Sidebar.item("Categories", url=url_for('menu.categories'), icon="category") }}

    {{ Sidebar.divider() }}

    {% call Sidebar.collapsible("Reports", icon="analytics") %}
        {{ Sidebar.item("Daily Sales", url="/reports/daily") }}
        {{ Sidebar.item("Weekly Summary", url="/reports/weekly") }}
    {% endcall %}

    {{ Sidebar.subheader("Configuration") }}
    {{ Sidebar.item("Settings", url=url_for('menu.settings'), icon="settings") }}
{% endcall %}
```

---

## Footer (`components/_footer.html`)

Footer navigation bar for page actions.

```jinja
{% import "components/_footer.html" as Footer %}
```

### Macros

| Macro | Parameters | Description |
|-------|------------|-------------|
| `render()` | - | Footer container (use with `{% call %}`) |
| `item(label, icon, url, modal, dropdown)` | `label`, `icon`, `url`, `modal`, `dropdown` | Footer action item |

### Example

```jinja
{% call Footer.render() %}
    {{ Footer.item("Back", "arrow_back", url_for('menu.index')) }}
    {{ Footer.item("Save", "save", modal="saveModal") }}
    {{ Footer.item("More", "more_vert", dropdown="actions-dropdown") }}
{% endcall %}
```
