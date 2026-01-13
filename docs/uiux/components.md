# Component Patterns

> Buttons, layouts, and cart components

---

## Buttons

### Primary Button

```html
<button type="button" class="pos-btn pos-btn-primary">Add to Order</button>
```

### Secondary Button

```html
<button type="button" class="pos-btn pos-btn-secondary">Cancel</button>
```

### Danger Button

```html
<button type="button" class="pos-btn pos-btn-danger">Void Item</button>
```

### Icon Button

```html
<button type="button" class="pos-btn pos-btn-icon" aria-label="Print receipt">
  <span class="material-symbols-rounded" aria-hidden="true">print</span>
</button>
```

### Large Touch Button

```html
<button type="button" class="pos-btn pos-btn-primary pos-btn-lg">Complete Order - $45.99</button>
```

---

## POS Terminal Layout

```html
<div class="pos-terminal">
  <main class="pos-menu-panel" role="main">
    <nav class="pos-category-nav" aria-label="Menu categories"><!-- tabs --></nav>
    <div class="pos-menu-grid" role="list" aria-label="Menu items"><!-- items --></div>
  </main>

  <aside class="pos-cart-panel" aria-label="Current order">
    <header class="pos-cart-header"><h2>Current Order</h2></header>
    <ul class="pos-cart-items" aria-label="Order items"><!-- items --></ul>
    <footer class="pos-cart-footer">
      <div class="pos-cart-total" aria-live="polite">Total: <strong>$45.99</strong></div>
      <button type="button" class="pos-btn pos-btn-primary pos-btn-lg">Pay Now</button>
    </footer>
  </aside>
</div>
```

---

## Cart Item

```html
<li class="pos-cart-item">
  <div class="pos-cart-item-info">
    <span class="pos-cart-item-qty">2x</span>
    <span class="pos-cart-item-name">Caesar Salad</span>
    <span class="pos-cart-item-mods">No croutons, dressing on side</span>
  </div>
  <div class="pos-cart-item-actions">
    <span class="pos-cart-item-price">$25.98</span>
    <button type="button" class="pos-btn pos-btn-icon pos-btn-sm" aria-label="Edit Caesar Salad">
      <span class="material-symbols-rounded" aria-hidden="true">edit</span>
    </button>
    <button type="button" class="pos-btn pos-btn-icon pos-btn-sm pos-btn-danger" aria-label="Remove Caesar Salad">
      <span class="material-symbols-rounded" aria-hidden="true">delete</span>
    </button>
  </div>
</li>
```
