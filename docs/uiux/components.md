# Component Patterns

> Materialize CSS components with POS-specific additions

---

## Philosophy: Materialize First

1. **Use Materialize CSS** for standard components (buttons, cards, modals)
2. **Use utility classes** for flex layouts (no prefix)
3. **Use plain descriptive names** for custom components (no prefix, no BEM)
4. **Use CSS nesting** for child elements and modifiers

---

## Buttons (Materialize CSS)

All buttons use Materialize CSS classes. Touch targets are enforced via `override.css`.

### Button Types

```html
<!-- Primary action -->
<button type="button" class="btn filled waves-effect waves-light">Add to Order</button>

<!-- Secondary action -->
<button type="button" class="btn tonal waves-effect waves-light">Cancel</button>

<!-- Outlined action -->
<button type="button" class="btn outlined waves-effect waves-light">Details</button>

<!-- Danger action -->
<button type="button" class="btn filled waves-effect waves-light"
        style="--md-sys-color-primary: var(--md-sys-color-error);">Void Item</button>

<!-- Text-only action -->
<button type="button" class="btn text waves-effect">Skip</button>
```

### Button with Icon

```html
<button type="button" class="btn filled waves-effect waves-light">
    <span class="material-symbols-rounded left" aria-hidden="true">print</span>
    Print Receipt
</button>
```

### Icon-Only Button

```html
<button type="button" class="btn-floating waves-effect waves-light" aria-label="Print receipt">
    <span class="material-symbols-rounded" aria-hidden="true">print</span>
</button>
```

### Large Touch Button (POS Actions)

```html
<button type="button" class="btn-large filled waves-effect waves-light">Complete Order - $45.99</button>
```

### Using Button Macros (Recommended)

```jinja2
{% import "macros/button.html" as Button %}

{{ Button.filled("Add to Order", url="/order/add", icon="add_shopping_cart") }}
{{ Button.tonal("Cancel", url="/cancel") }}
{{ Button.submit("Save", icon="save") }}
```

---

## Cards (Materialize CSS)

```html
<div class="card">
    <div class="card-content">
        <span class="card-title">Card Title</span>
        <p>Card content here.</p>
    </div>
    <div class="card-action">
        <a href="#" class="btn text waves-effect">Action</a>
    </div>
</div>
```

---

## Modals (Materialize CSS)

```html
<div id="modal1" class="modal">
    <div class="modal-content">
        <h4>Modal Header</h4>
        <p>Modal content here.</p>
    </div>
    <div class="modal-footer">
        <button type="button" class="btn text waves-effect" data-dismiss="modal">Cancel</button>
        <button type="button" class="btn filled waves-effect waves-light">Confirm</button>
    </div>
</div>
```

---

## Custom Components

Custom components use plain descriptive class names with CSS nesting for structure.

### Terminal Layout

```html
<div class="terminal">
    <main class="menu-panel" role="main">
        <nav class="category-nav" aria-label="Menu categories"><!-- tabs --></nav>
        <div class="menu-grid" role="list" aria-label="Menu items"><!-- items --></div>
    </main>

    <aside class="cart-panel" aria-label="Current order">
        <header class="cart-header"><h2>Current Order</h2></header>
        <ul class="cart-items" aria-label="Order items"><!-- items --></ul>
        <footer class="cart-footer">
            <div class="cart-total" aria-live="polite">Total: <strong>$45.99</strong></div>
            <button type="button" class="btn-large filled waves-effect waves-light">Pay Now</button>
        </footer>
    </aside>
</div>
```

```css
/* CSS uses nesting for child elements */
.terminal {
  & .menu-panel { /* ... */ }
  & .cart-panel { /* ... */ }
}
```

### Cart Item

```html
<li class="cart-item">
    <div class="info">
        <span class="qty">2x</span>
        <span class="name">Caesar Salad</span>
        <span class="mods">No croutons, dressing on side</span>
    </div>
    <div class="actions">
        <span class="price">$25.98</span>
        <button type="button" class="btn-floating btn-small waves-effect" aria-label="Edit Caesar Salad">
            <span class="material-symbols-rounded" aria-hidden="true">edit</span>
        </button>
        <button type="button" class="btn-floating btn-small waves-effect" aria-label="Remove Caesar Salad">
            <span class="material-symbols-rounded" aria-hidden="true">delete</span>
        </button>
    </div>
</li>
```

```css
/* CSS nesting replaces BEM naming */
.cart-item {
  & .info { /* ... */ }
  & .qty { /* ... */ }
  & .name { /* ... */ }
  & .mods { /* ... */ }
  & .actions { /* ... */ }
  & .price { /* ... */ }
}
```
