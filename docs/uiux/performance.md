# Performance

> Targets, JavaScript patterns, and CSS optimization

---

## Targets

| Metric | Target |
|--------|--------|
| First Contentful Paint | < 1.0s |
| Largest Contentful Paint | < 1.5s |
| Time to Interactive | < 2.0s |
| Cumulative Layout Shift | < 0.1 |
| JS Bundle (gzipped) | < 100KB |
| CSS Bundle (gzipped) | < 50KB |

---

## JavaScript Patterns

### Event Delegation

```javascript
document.getElementById('menu-grid').addEventListener('click', (e) => {
  const item = e.target.closest('.pos-menu-item');
  if (item) handleMenuItemClick(item);
});
```

### Debounce Expensive Operations

```javascript
function debounce(fn, delay = 150) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}
```

### Visual Updates

```javascript
requestAnimationFrame(() => renderCartItems(items));
```

### Lazy Load Modules

```javascript
const { ReportManager } = await import('./modules/reports/index.js');
```

---

## CSS Patterns

### Avoid Expensive Selectors

```css
/* Bad */
.pos-grid > * > .pos-item { }

/* Good */
.pos-grid-item { }
```

### Use Transform/Opacity for Animations

```css
.pos-slide-in {
  transform: translateX(100%);
  transition: transform 0.3s ease-out;
}
.pos-slide-in.is-visible {
  transform: translateX(0);
}
```

### Contain Paint for Isolated Components

```css
.pos-cart-panel {
  contain: layout paint;
}
```
