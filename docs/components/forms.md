# Forms Component

> Auto-renders WTForms with MaterializeCSS styling.

```jinja
{% import "macros/forms.html" as Forms %}
```

---

## Macros

| Macro | Parameters | Description |
|-------|------------|-------------|
| `render(form, extra_wrappers)` | `form`, `extra_wrappers={}` | Renders entire form |
| `render_field_auto(field, extra_wrap)` | `field`, `extra_wrap=''` | Renders single field |

---

## Supported Field Types

- `StringField`, `PasswordField`, `EmailField`, `SearchField`
- `IntegerField`, `DecimalField`, `FloatField`
- `DateField`, `DateTimeLocalField`
- `TextAreaField`, `SelectField`, `SelectMultipleField`
- `BooleanField` (checkbox or switch)
- `FileField`, `SubmitField`
- `FieldList`, `FormField` (nested forms)

---

## Examples

### Basic Usage

```jinja
<form method="post">
    {{ Forms.render(form) }}
</form>
```

### With Custom Column Widths

```jinja
<form method="post">
    {{ Forms.render(form, {'name': 'm6', 'email': 'm6'}) }}
</form>
```

### Switch Toggle

```python
# In forms.py
is_active = BooleanField('Active', render_kw={'render_as': 'switch'})
```
