# Accessibility (WCAG 2.1 AA)

> Requirements, ARIA patterns, and screen reader support

---

## Requirements

| Requirement | Standard |
|-------------|----------|
| Color Contrast | 4.5:1 normal text, 3:1 large text |
| Focus Indicators | Visible focus rings on all interactive elements |
| Keyboard Navigation | All functionality via keyboard |
| Touch Targets | Minimum 44x44px |
| Screen Reader | Proper ARIA labels and live regions |
| Reduced Motion | Respect `prefers-reduced-motion` |

---

## Focus Ring

```css
.pos-focus-ring:focus-visible {
  outline: 3px solid var(--pos-primary);
  outline-offset: 2px;
}
.pos-focus-ring:focus { outline: none; }
```

---

## ARIA Patterns

### Live Region for Updates

```html
<div role="status" aria-live="polite" class="pos-sr-only" id="order-status"></div>
```

### Button with State

```html
<button type="button" aria-pressed="false" aria-describedby="price-123">Item</button>
```

### Modal Dialog

```html
<dialog class="pos-modal" aria-labelledby="modal-title" aria-describedby="modal-desc">
  <h2 id="modal-title">Title</h2>
  <p id="modal-desc">Description</p>
</dialog>
```

---

## Screen Reader Only

```css
.pos-sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

---

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```
