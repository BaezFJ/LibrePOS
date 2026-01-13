# Action Bar Component

> Floating action toolbar for page actions.

```jinja
{% import "macros/action_bar.html" as ActionBar %}
```

---

## Macros

| Macro | Parameters | Description |
|-------|------------|-------------|
| `render(...)` | See below | Main action bar container |
| `item(label, icon, url, modal, dropdown, _class)` | See below | Individual action button |
| `divider()` | - | Vertical divider |

---

## Render Parameters

| Parameter | Description |
|-----------|-------------|
| `id` | Container ID (default: `action-bar`) |
| `create_label`, `create_icon`, `create_url`, `create_modal` | Create action config |
| `filter_label`, `filter_icon`, `filter_dropdown`, `filter_url` | Filter action config |
| `sort_label`, `sort_icon`, `sort_dropdown`, `sort_url` | Sort action config |
| `search_label`, `search_icon`, `search_modal`, `search_url` | Search action config |

---

## Examples

### Standard Actions

```jinja
{{ ActionBar.render(
    create_modal="createItemModal",
    search_modal="searchModal",
    filter_dropdown="filter-dropdown",
    sort_dropdown="sort-dropdown"
) }}
```

### Custom Actions

```jinja
{% call ActionBar.render(id="item-actions") %}
    {{ ActionBar.item("Edit", "edit", modal="editModal") }}
    {{ ActionBar.item("Duplicate", "content_copy", url=url_for('menu.duplicate', id=item.id)) }}
    {{ ActionBar.divider() }}
    {{ ActionBar.item("Delete", "delete", modal="deleteModal", _class="red-text") }}
{% endcall %}
```

---

# Breadcrumbs Component

> Navigation breadcrumbs (auto-rendered from context).

```jinja
{% include "macros/breadcrumbs.html" %}
```

---

## Usage

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
