# Icon Component

> Material Symbols icon helper with semantic macros for POS consistency.

```jinja
{% import "macros/icon.html" as Icon %}
```

---

## Base Macro

| Macro | Parameters | Description |
|-------|------------|-------------|
| `render(name, class_, attrs)` | `name`, `class_=None`, `attrs=None` | Renders any icon by name |

---

## Semantic Icon Macros

All semantic macros accept `(class_=None, attrs=None)` parameters.

### CRUD Operations

| Macro | Icon | Usage |
|-------|------|-------|
| `add()` | add | Create new items |
| `edit()` | edit | Edit existing items |
| `delete()` | delete | Delete/remove items |
| `save()` | save | Save changes |
| `cancel()` | cancel | Cancel/discard |

### Navigation

| Macro | Icon | Usage |
|-------|------|-------|
| `back()` | arrow_back | Go back |
| `close()` | close | Close modal/panel |
| `menu()` | menu | Hamburger menu |
| `home()` | home | Home/dashboard |
| `more()` | more_vert | More options |

### Orders & POS

| Macro | Icon | Usage |
|-------|------|-------|
| `order()` | receipt_long | Orders |
| `cart()` | shopping_cart | Cart/basket |
| `payment()` | payments | Payment |
| `cash()` | attach_money | Cash payment |
| `card()` | credit_card | Card payment |
| `table()` | table_restaurant | Table |
| `receipt()` | receipt | Receipt/check |
| `discount()` | percent | Discount |
| `tip()` | volunteer_activism | Tip |

### Menu Management

| Macro | Icon | Usage |
|-------|------|-------|
| `food()` | restaurant_menu | Food items |
| `drink()` | local_bar | Beverages |
| `category()` | category | Categories |
| `modifier()` | tune | Modifiers |
| `price()` | sell | Pricing |

### Kitchen

| Macro | Icon | Usage |
|-------|------|-------|
| `kitchen()` | soup_kitchen | Kitchen display |
| `timer()` | timer | Cook time |
| `done()` | check_circle | Order ready |
| `priority()` | priority_high | Rush order |

### Staff & Users

| Macro | Icon | Usage |
|-------|------|-------|
| `user()` | person | Single user |
| `users()` | groups | Multiple users |
| `login()` | login | Sign in |
| `logout()` | logout | Sign out |
| `role()` | admin_panel_settings | Roles/permissions |

### Status Indicators

| Macro | Icon | Usage |
|-------|------|-------|
| `success()` | check_circle | Success state |
| `error()` | error | Error state |
| `warning()` | warning | Warning state |
| `info()` | info | Information |
| `pending()` | hourglass_empty | Pending/waiting |

### Common Actions

| Macro | Icon | Usage |
|-------|------|-------|
| `search()` | search | Search |
| `filter()` | filter_list | Filter |
| `sort()` | sort | Sort |
| `refresh()` | refresh | Refresh/reload |
| `print_()` | print | Print |
| `export()` | download | Export/download |
| `settings()` | settings | Settings |
| `help_()` | help | Help |

---

## Examples

```jinja
{# Generic (still works) #}
{{ Icon.render("add") }}
{{ Icon.render("delete", "red-text") }}

{# Semantic (recommended) #}
{{ Icon.add() }}
{{ Icon.delete(class_="red-text") }}
{{ Icon.save(class_="left") }}
{{ Icon.cart() }}
```
