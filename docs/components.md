# UI Components

> Jinja2 macro library for building consistent UI in LibrePOS

---

## Overview

LibrePOS uses reusable Jinja2 macros for UI components:

- **Layout Components** (`templates/components/`) - Page structure elements
- **Macro Components** (`templates/macros/`) - Reusable UI patterns

All components use [Bootstrap](https://getbootstrap.com/) and [Material Symbols](https://fonts.google.com/icons) icons.

---

## Quick Reference

### Layout Components

| Component | Import | Purpose |
|-----------|--------|---------|
| Navbar | `{% import "components/_navbar.html" as Navbar %}` | Top navigation bar |
| Sidebar | `{% import "components/_sidebar.html" as Sidebar with context %}` | Side navigation |
| Footer | `{% import "components/_footer.html" as Footer %}` | Footer action bar |
| Dropdown | `{% import "components/_dropdown.html" as Dropdown %}` | Dropdown menus |

### Macro Components

| Component | Import | Purpose |
|-----------|--------|---------|
| Icon | `{% import "macros/icon.html" as Icon %}` | Material Symbols icons |
| Badge | `{% import "macros/badge.html" as Badge %}` | Status indicators |
| Button | `{% import "macros/button.html" as Button %}` | Buttons and links |
| Forms | `{% import "macros/forms.html" as Forms %}` | WTForms rendering |
| Modal | `{% import "macros/modals.html" as Modal %}` | Dialog windows |
| ActionBar | `{% import "macros/action_bar.html" as ActionBar %}` | Floating toolbar |
| Breadcrumbs | `{% include "macros/breadcrumbs.html" %}` | Navigation trail |

---

## Component Summary

### Navbar

```jinja
{% call Navbar.render() %}
    {{ Navbar.title("Page Title") }}
    <ul class="right">
        {{ Navbar.item("Home", "home", url_for('main.index')) }}
    </ul>
{% endcall %}
```

### Sidebar

```jinja
{% call Sidebar.render() %}
    {{ Sidebar.item("Dashboard", url=url_for('main.index'), icon="dashboard") }}
    {{ Sidebar.subheader("Section") }}
    {{ Sidebar.item("Settings", url="/settings", icon="settings") }}
{% endcall %}
```

### Icon

```jinja
{{ Icon.add() }}
{{ Icon.edit() }}
{{ Icon.delete(class_="red-text") }}
{{ Icon.render("custom_icon") }}
```

### Badge

```jinja
{{ Badge.pending() }}
{{ Badge.completed() }}
{{ Badge.count(5) }}
{{ Badge.success("Active") }}
```

### Button

```jinja
{{ Button.filled("Save", url="/save", icon="save") }}
{{ Button.outlined("Cancel", url="/cancel") }}
{{ Button.submit("Submit", icon="send") }}
```

### Forms

```jinja
<form method="post">
    {{ Forms.render(form) }}
</form>
```

### Modal

```jinja
{{ Modal.trigger("my-modal", "Open", "open_in_new") }}
{% call Modal.render("my-modal", "Modal Title") %}
    <p>Modal content here</p>
{% endcall %}
```

### Action Bar

```jinja
{{ ActionBar.render(
    create_modal="createModal",
    search_modal="searchModal"
) }}
```

---

## Best Practices

1. **Import at top** - Import macros at the beginning of templates
2. **Use semantic icons** - Choose Material Symbols that convey meaning
3. **Consistent naming** - Use `modal_id` pattern: `createItemModal`, `deleteUserModal`
4. **Accessibility** - Modals and dropdowns include ARIA attributes
5. **Mobile-first** - Components are responsive by default

---

## Detailed Documentation

- [Layout Components](components/layout.md) - Navbar, Sidebar, Footer
- [Dropdown](components/dropdown.md) - Dropdown menus and app grids
- [Icons](components/icons.md) - Semantic icon macros
- [Badges](components/badges.md) - Status and notification badges
- [Buttons](components/buttons.md) - Button types and variants
- [Forms](components/forms.md) - WTForms auto-rendering
- [Modals](components/modals.md) - Dialogs and confirmations
- [Action Bar & Breadcrumbs](components/action-bar.md) - Toolbar and navigation
