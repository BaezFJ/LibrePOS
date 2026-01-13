# Modal Component

> Dialog components for confirmations, forms, and search.

```jinja
{% import "macros/modals.html" as Modal %}
```

---

## Macros

| Macro | Parameters | Description |
|-------|------------|-------------|
| `trigger(modal_id, label, icon, _class)` | `modal_id`, `label`, `icon`, `_class` | Button to open modal |
| `render(modal_id, title, _class)` | `modal_id`, `title`, `_class` | Basic modal (use with `{% call %}`) |
| `form_modal(modal_id, title, action, method, _class, submit_text)` | See below | Modal with form |
| `confirmation(...)` | See below | Confirmation dialog |
| `search(modal_id, action, placeholder, param, clear_url)` | See below | Search modal |

---

## Examples

### Basic Modal

```jinja
{{ Modal.trigger("help-modal", "Help", "help") }}

{% call Modal.render("help-modal", "Help & Support") %}
    <p>Contact support at support@example.com</p>
{% endcall %}
```

### Form Modal

```jinja
{% call Modal.form_modal("create-category", "New Category", url_for('menu.create_category')) %}
    {{ Forms.render(category_form) }}
{% endcall %}
```

### Confirmation Dialog

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

### Confirmation with Password

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

### Search Modal

```jinja
{{ Modal.search(
    modal_id="search",
    action=url_for('menu.items'),
    placeholder="Search menu items..."
) }}
```
