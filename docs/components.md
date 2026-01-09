# UI Components

> Jinja2 macro library for building consistent UI in LibrePOS

## Overview

LibrePOS uses reusable Jinja2 macros for UI components. Components are organized into:

- **Layout Components** (`templates/components/`) - Page structure elements
- **Macro Components** (`templates/macros/`) - Reusable UI patterns

All components use [MaterializeCSS](https://materializeweb.com/) and [Material Symbols](https://fonts.google.com/icons) icons.

---

## Layout Components

### Navbar (`components/_navbar.html`)

Top navigation bar with support for dropdowns and mobile triggers.

```jinja
{% import "components/_navbar.html" as Navbar %}
```

#### Macros

| Macro | Parameters | Description |
|-------|------------|-------------|
| `render()` | - | Container wrapper (use with `{% call %}`) |
| `title(text)` | `text` | Centered brand title |
| `item(label, icon, url, dynamic)` | `label`, `icon`, `url`, `dynamic=True` | Nav item link |
| `dropdown_trigger(label, icon, target)` | `label`, `icon`, `target` | Dropdown trigger button |
| `dropdown(label, icon, target, class_)` | `label`, `icon`, `target`, `class_` | Full dropdown with trigger |
| `dropdown_item(label, icon, url)` | `label`, `icon`, `url` | Item inside dropdown |
| `sidenav_trigger(target)` | `target="mainMenu"` | Mobile sidenav toggle |

#### Example

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

### Sidebar (`components/_sidebar.html`)

Fixed side navigation with collapsible sections.

```jinja
{% import "components/_sidebar.html" as Sidebar %}
```

#### Macros

| Macro | Parameters | Description |
|-------|------------|-------------|
| `render(title, id)` | `title`, `id="mainMenu"` | Sidenav container (use with `{% call %}`) |
| `item(label, icon, url, active)` | `label`, `icon`, `url`, `active=False` | Nav item (auto-detects active state) |
| `collapsible(text, icon)` | `text`, `icon` | Collapsible section (use with `{% call %}`) |
| `divider()` | - | Horizontal divider |
| `subheader(label)` | `label` | Section subheader |

#### Example

```jinja
{% call Sidebar.render("LibrePOS", "mainMenu") %}
    {{ Sidebar.subheader("Main") }}
    {{ Sidebar.item("Dashboard", "dashboard", url_for('main.dashboard')) }}
    {{ Sidebar.item("Orders", "receipt_long", url_for('orders.index')) }}

    {{ Sidebar.divider() }}
    {{ Sidebar.subheader("Management") }}

    {% call Sidebar.collapsible("Menu", "restaurant_menu") %}
        {{ Sidebar.item("Items", "inventory_2", url_for('menu.items')) }}
        {{ Sidebar.item("Categories", "category", url_for('menu.categories')) }}
    {% endcall %}
{% endcall %}
```

---

### Footer (`components/_footer.html`)

Footer navigation bar for page actions.

```jinja
{% import "components/_footer.html" as Footer %}
```

#### Macros

| Macro | Parameters | Description |
|-------|------------|-------------|
| `render()` | - | Footer container (use with `{% call %}`) |
| `item(label, icon, url, modal, dropdown)` | `label`, `icon`, `url`, `modal`, `dropdown` | Footer action item |

#### Example

```jinja
{% call Footer.render() %}
    {{ Footer.item("Back", "arrow_back", url_for('menu.index')) }}
    {{ Footer.item("Save", "save", modal="saveModal") }}
    {{ Footer.item("More", "more_vert", dropdown="actions-dropdown") }}
{% endcall %}
```

---

### Dropdown (`components/_dropdown.html`)

Dropdown menus for actions and app grids.

```jinja
{% import "components/_dropdown.html" as Dropdown %}
```

#### Macros

| Macro | Parameters | Description |
|-------|------------|-------------|
| `render(id, class_)` | `id`, `class_=None` | Dropdown container (use with `{% call %}`) |
| `trigger(id, icon, aria_label)` | `id`, `icon`, `aria_label` | Trigger button |
| `item(label, url, icon, badge, _class)` | `label`, `url`, `icon`, `badge`, `_class` | Menu item |
| `tile(icon, label, url)` | `icon`, `label`, `url` | App grid tile |
| `divider()` | - | Horizontal divider |

#### Example: Actions Menu

```jinja
{{ Dropdown.trigger("actions-menu", "more_vert", "Actions") }}

{% call Dropdown.render("actions-menu") %}
    {{ Dropdown.item("Edit", url_for('menu.edit', id=item.id), "edit") }}
    {{ Dropdown.item("Duplicate", url_for('menu.duplicate', id=item.id), "content_copy") }}
    {{ Dropdown.divider() }}
    {{ Dropdown.item("Delete", url_for('menu.delete', id=item.id), "delete", _class="red-text") }}
{% endcall %}
```

#### Example: Apps Grid

```jinja
{% call Dropdown.render("apps-dropdown", "apps-dropdown") %}
    <li>
        <div class="apps-dropdown-inner">
            <div class="apps-grid">
                {{ Dropdown.tile("point_of_sale", "POS", url_for('orders.pos')) }}
                {{ Dropdown.tile("restaurant_menu", "Menu", url_for('menu.index')) }}
                {{ Dropdown.tile("groups", "Staff", url_for('staff.index')) }}
            </div>
        </div>
    </li>
{% endcall %}
```

---

## Macro Components

### Icon (`macros/icon.html`)

Material Symbols icon helper.

```jinja
{% import "macros/icon.html" as Icon %}
```

#### Macro

| Macro | Parameters | Description |
|-------|------------|-------------|
| `render(name, class_, attrs)` | `name`, `class_=None`, `attrs=None` | Renders icon element |

#### Example

```jinja
{{ Icon.render("add") }}
{{ Icon.render("delete", "red-text") }}
{{ Icon.render("info", "left", 'data-tooltip="Help"') }}
```

---

### Forms (`macros/forms.html`)

Auto-renders WTForms with MaterializeCSS styling.

```jinja
{% import "macros/forms.html" as Forms %}
```

#### Macros

| Macro | Parameters | Description |
|-------|------------|-------------|
| `render(form, extra_wrappers)` | `form`, `extra_wrappers={}` | Renders entire form |
| `render_field_auto(field, extra_wrap)` | `field`, `extra_wrap=''` | Renders single field |

#### Supported Field Types

- `StringField`, `PasswordField`, `EmailField`, `SearchField`
- `IntegerField`, `DecimalField`, `FloatField`
- `DateField`, `DateTimeLocalField`
- `TextAreaField`, `SelectField`, `SelectMultipleField`
- `BooleanField` (checkbox or switch)
- `FileField`, `SubmitField`
- `FieldList`, `FormField` (nested forms)

#### Example

```jinja
<form method="post">
    {{ Forms.render(form) }}
</form>

{# With custom column widths #}
<form method="post">
    {{ Forms.render(form, {'name': 'm6', 'email': 'm6'}) }}
</form>
```

#### Switch Toggle

```python
# In forms.py
is_active = BooleanField('Active', render_kw={'render_as': 'switch'})
```

---

### Modals (`macros/modals.html`)

Dialog components for confirmations, forms, and search.

```jinja
{% import "macros/modals.html" as Modal %}
```

#### Macros

| Macro | Parameters | Description |
|-------|------------|-------------|
| `trigger(modal_id, label, icon, _class)` | `modal_id`, `label`, `icon`, `_class` | Button to open modal |
| `render(modal_id, title, _class)` | `modal_id`, `title`, `_class` | Basic modal (use with `{% call %}`) |
| `form_modal(modal_id, title, action, method, _class, submit_text)` | See below | Modal with form |
| `confirmation(...)` | See below | Confirmation dialog |
| `search(modal_id, action, placeholder, param, clear_url)` | See below | Search modal |

#### Example: Basic Modal

```jinja
{{ Modal.trigger("help-modal", "Help", "help") }}

{% call Modal.render("help-modal", "Help & Support") %}
    <p>Contact support at support@example.com</p>
{% endcall %}
```

#### Example: Form Modal

```jinja
{% call Modal.form_modal("create-category", "New Category", url_for('menu.create_category')) %}
    {{ Forms.render(category_form) }}
{% endcall %}
```

#### Example: Confirmation

```jinja
{{ Modal.confirmation(
    modal_id="delete-item",
    title="Delete Item",
    action=url_for('menu.delete', id=item.id),
    message="Are you sure you want to delete <strong>" ~ item.name ~ "</strong>?",
    warning="This action cannot be undone.",
    confirm_text="Delete",
    confirm_icon="delete",
    confirm_color="red"
) }}
```

#### Example: Confirmation with Password

```jinja
{{ Modal.confirmation(
    modal_id="delete-account",
    title="Delete Account",
    action=url_for('staff.delete_account'),
    message="This will permanently delete your account.",
    require_password=true,
    confirm_text="Delete Account",
    confirm_color="red"
) }}
```

#### Example: Search Modal

```jinja
{{ Modal.search(
    modal_id="search",
    action=url_for('menu.items'),
    placeholder="Search menu items..."
) }}
```

---

### Action Bar (`macros/action_bar.html`)

Floating action toolbar for page actions.

```jinja
{% import "macros/action_bar.html" as ActionBar %}
```

#### Macros

| Macro | Parameters | Description |
|-------|------------|-------------|
| `render(...)` | See below | Main action bar container |
| `item(label, icon, url, modal, dropdown, _class)` | See below | Individual action button |
| `divider()` | - | Vertical divider |

#### Render Parameters

| Parameter | Description |
|-----------|-------------|
| `id` | Container ID (default: `action-bar`) |
| `create_label`, `create_icon`, `create_url`, `create_modal` | Create action config |
| `filter_label`, `filter_icon`, `filter_dropdown`, `filter_url` | Filter action config |
| `sort_label`, `sort_icon`, `sort_dropdown`, `sort_url` | Sort action config |
| `search_label`, `search_icon`, `search_modal`, `search_url` | Search action config |

#### Example: Standard Actions

```jinja
{{ ActionBar.render(
    create_modal="createItemModal",
    search_modal="searchModal",
    filter_dropdown="filter-dropdown",
    sort_dropdown="sort-dropdown"
) }}
```

#### Example: Custom Actions

```jinja
{% call ActionBar.render(id="item-actions") %}
    {{ ActionBar.item("Edit", "edit", modal="editModal") }}
    {{ ActionBar.item("Duplicate", "content_copy", url=url_for('menu.duplicate', id=item.id)) }}
    {{ ActionBar.divider() }}
    {{ ActionBar.item("Delete", "delete", modal="deleteModal", _class="red-text") }}
{% endcall %}
```

---

### Breadcrumbs (`macros/breadcrumbs.html`)

Navigation breadcrumbs (auto-rendered from context).

```jinja
{% include "macros/breadcrumbs.html" %}
```

#### Usage

Pass `breadcrumb` list in view context:

```python
@bp.route('/items/<int:id>')
def item_detail(id):
    item = MenuItem.query.get_or_404(id)
    return render_template('menu/item_detail.html',
        item=item,
        breadcrumb=[
            {"url": url_for("menu.index"), "label": "Menu"},
            {"url": url_for("menu.items"), "label": "Items"},
            {"url": None, "label": item.name}  # Current page (no link)
        ]
    )
```

Renders as: `Menu > Items > Item Name`

---

## Best Practices

1. **Import at top** - Import macros at the beginning of templates
2. **Use semantic icons** - Choose Material Symbols that convey meaning
3. **Consistent naming** - Use `modal_id` pattern: `createItemModal`, `deleteUserModal`
4. **Accessibility** - Modals and dropdowns include ARIA attributes
5. **Mobile-first** - Components are responsive by default
