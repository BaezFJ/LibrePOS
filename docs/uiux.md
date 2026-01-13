# LibrePOS UI/UX Guidelines

Modern POS system built with Flask, Jinja2, Materialize CSS 2.2.2, and vanilla JavaScript (ES2022+).

## Quick Reference

| Task | Implementation |
|------|----------------|
| Add theme support | Use `var(--pos-*)` custom properties |
| Make touchable | Min 48x48px, use `pointerdown`/`pointerup` |
| Add to screen reader | Use `aria-label`, `aria-live`, `role` |
| Animate safely | Use `transform`/`opacity`, check `prefers-reduced-motion` |
| Handle state | Use `data-*` attributes and `aria-*` states |
| Add icon | `<span class="material-symbols-rounded" aria-hidden="true">icon_name</span>` |

### CSS Files

| File | Purpose |
|------|---------|
| `variables.css` | Design tokens (Catppuccin colors, spacing, typography) |
| `main.css` | Global layout, navigation, components |
| `utilities.css` | Utility classes (flexbox, colors) |
| `override.css` | Materialize CSS overrides |

### Class Prefixes

| Prefix | Purpose |
|--------|---------|
| `.pos-` | All LibrePOS components |
| `.pos-btn-` | Button variants |
| `.pos-card-` | Card components |
| `.pos-menu-` | Menu-related components |
| `.pos-cart-` | Cart/order components |
| `.pos-modal-` | Modal dialogs |
| `.pos-sr-` | Screen reader utilities |

---

## Core Principles

- **Mobile & Touch First**: Design for touch before mouse/keyboard
- **Restaurant-Optimized**: Fast-paced environment patterns
- **Accessibility First**: WCAG 2.1 AA mandatory
- **Performance Obsessed**: Sub-second interactions

---

## Project Structure

```
app/
├── blueprints/{name}/
│   ├── static/css/        # Blueprint-specific styles
│   ├── static/js/         # Blueprint-specific scripts
│   └── templates/{name}/  # Blueprint templates
├── static/
│   ├── vendor/            # Materialize, Material Symbols, Chart.js, SortableJS, interact.js
│   ├── css/               # variables.css, main.css, utilities.css, override.css
│   ├── js/                # app.js, utils.js, sw.js
│   └── img/
└── templates/
    ├── base.html          # Master layout
    ├── layouts/           # admin, pos, kds layouts
    ├── components/        # Reusable Jinja2 components
    ├── macros/            # Jinja2 macro libraries
    └── errors/            # Error pages
```

---

## Design System

### Color Palette (Catppuccin)

All colors defined in `app/static/css/variables.css`. Light theme uses Catppuccin Latte, dark theme uses Catppuccin Mocha.

**Brand Colors:**
- `--pos-primary`: Blue (`#1e66f5` light / `#89b4fa` dark)
- `--pos-secondary`: Overlay (`#9ca0b0` light / `#6c7086` dark)
- `--pos-accent`: Teal (`#179299` light / `#94e2d5` dark)

**Semantic Colors:**
- `--pos-success`: Green
- `--pos-warning`: Yellow
- `--pos-danger`: Red
- `--pos-info`: Sapphire

**Surface Colors:**
- `--pos-bg-primary`: Base background
- `--pos-bg-secondary`: Mantle (cards, panels)
- `--pos-bg-tertiary`: Surface0 (elevated elements)

**Text Colors:**
- `--pos-text-primary`: Main text
- `--pos-text-secondary`: Secondary text
- `--pos-text-muted`: Disabled/hint text

**Borders:**
- `--pos-border`: Default border
- `--pos-border-strong`: Emphasized border

**Additional Catppuccin colors** available via `--ctp-*` variables: rosewater, flamingo, pink, mauve, maroon, peach, sky, lavender.

### Typography

```css
--pos-font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--pos-font-mono: ui-monospace, 'SF Mono', Monaco, 'Cascadia Code', monospace;

/* Sizes */
--pos-text-xs: 0.75rem;    /* 12px - minimum for labels */
--pos-text-sm: 0.875rem;   /* 14px */
--pos-text-base: 1rem;     /* 16px - body text minimum */
--pos-text-lg: 1.125rem;   /* 18px */
--pos-text-xl: 1.25rem;    /* 20px */
--pos-text-2xl: 1.5rem;    /* 24px */
--pos-text-3xl: 1.875rem;  /* 30px */
--pos-text-4xl: 2.25rem;   /* 36px */
```

### Spacing Scale

```css
--pos-space-1: 0.25rem;   /* 4px */
--pos-space-2: 0.5rem;    /* 8px */
--pos-space-3: 0.75rem;   /* 12px */
--pos-space-4: 1rem;      /* 16px */
--pos-space-5: 1.25rem;   /* 20px */
--pos-space-6: 1.5rem;    /* 24px */
--pos-space-8: 2rem;      /* 32px */
--pos-space-10: 2.5rem;   /* 40px */
--pos-space-12: 3rem;     /* 48px */
```

### Icons (Material Symbols Rounded)

Bundled locally in `app/static/vendor/google/`.

```html
<!-- Standard icon -->
<span class="material-symbols-rounded" aria-hidden="true">shopping_cart</span>

<!-- Filled variant -->
<span class="material-symbols-rounded filled" aria-hidden="true">favorite</span>
```

**Size variants:** `.pos-icon-sm` (20px), `.pos-icon-lg` (32px), `.pos-icon-xl` (48px)

---

## Touch & Responsive Design

### Touch Targets

- **Minimum**: 44x44px (WCAG 2.1 AAA)
- **Recommended**: 48x48px
- **Menu items**: 56px height (frequent taps)
- **Gap between targets**: 8px minimum

### Touch Interactions

```javascript
// Use pointer events for cross-device compatibility
element.addEventListener('pointerdown', () => element.classList.add('pos-active'));
element.addEventListener('pointerup', () => element.classList.remove('pos-active'));
element.addEventListener('pointerleave', () => element.classList.remove('pos-active'));
```

### Responsive Breakpoints

```css
/* Mobile First - Base styles are for mobile */
@media (min-width: 768px) { }   /* Tablet Portrait */
@media (min-width: 1024px) { }  /* Tablet Landscape / Small Desktop */
@media (min-width: 1280px) { }  /* Desktop */
@media (min-width: 1536px) { }  /* Large Desktop / POS Terminal */
```

### Device-Specific CSS

```css
.pos-interactive {
  -webkit-user-select: none;
  user-select: none;
  -webkit-touch-callout: none;
  -webkit-tap-highlight-color: transparent;
}

body { overscroll-behavior: none; }
```

---

## Theme System

Theme stored in `localStorage` key `pos-theme`. Toggle via `data-theme` attribute on `<html>`.

```javascript
// Set theme
document.documentElement.setAttribute('data-theme', 'dark');
localStorage.setItem('pos-theme', 'dark');

// Update browser chrome color
document.querySelector('meta[name="theme-color"]')
  ?.setAttribute('content', theme === 'dark' ? '#1e1e2e' : '#eff1f5');
```

---

## Accessibility (WCAG 2.1 AA)

### Requirements

- **Color Contrast**: 4.5:1 normal text, 3:1 large text
- **Focus Indicators**: Visible focus rings on all interactive elements
- **Keyboard Navigation**: All functionality via keyboard
- **Touch Targets**: Minimum 44x44px
- **Screen Reader**: Proper ARIA labels and live regions
- **Reduced Motion**: Respect `prefers-reduced-motion`

### Focus Ring

```css
.pos-focus-ring:focus-visible {
  outline: 3px solid var(--pos-primary);
  outline-offset: 2px;
}
.pos-focus-ring:focus { outline: none; }
```

### ARIA Patterns

```html
<!-- Live region for updates -->
<div role="status" aria-live="polite" class="pos-sr-only" id="order-status"></div>

<!-- Button with state -->
<button type="button" aria-pressed="false" aria-describedby="price-123">Item</button>

<!-- Modal dialog -->
<dialog class="pos-modal" aria-labelledby="modal-title" aria-describedby="modal-desc">
```

### Screen Reader Only

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

### Reduced Motion

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

---

## Performance

### Targets

| Metric | Target |
|--------|--------|
| First Contentful Paint | < 1.0s |
| Largest Contentful Paint | < 1.5s |
| Time to Interactive | < 2.0s |
| Cumulative Layout Shift | < 0.1 |
| JS Bundle (gzipped) | < 100KB |
| CSS Bundle (gzipped) | < 50KB |

### JavaScript Patterns

```javascript
// Event delegation
document.getElementById('menu-grid').addEventListener('click', (e) => {
  const item = e.target.closest('.pos-menu-item');
  if (item) handleMenuItemClick(item);
});

// Debounce expensive operations
function debounce(fn, delay = 150) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

// Visual updates
requestAnimationFrame(() => renderCartItems(items));

// Lazy load modules
const { ReportManager } = await import('./modules/reports/index.js');
```

### CSS Patterns

```css
/* Avoid expensive selectors */
/* Bad: */ .pos-grid > * > .pos-item { }
/* Good: */ .pos-grid-item { }

/* Use transform/opacity for animations */
.pos-slide-in { transform: translateX(100%); transition: transform 0.3s ease-out; }
.pos-slide-in.is-visible { transform: translateX(0); }

/* Contain paint for isolated components */
.pos-cart-panel { contain: layout paint; }
```

---

## Component Patterns

### Buttons

```html
<!-- Primary -->
<button type="button" class="pos-btn pos-btn-primary">Add to Order</button>

<!-- Secondary -->
<button type="button" class="pos-btn pos-btn-secondary">Cancel</button>

<!-- Danger -->
<button type="button" class="pos-btn pos-btn-danger">Void Item</button>

<!-- Icon button -->
<button type="button" class="pos-btn pos-btn-icon" aria-label="Print receipt">
  <span class="material-symbols-rounded" aria-hidden="true">print</span>
</button>

<!-- Large touch button -->
<button type="button" class="pos-btn pos-btn-primary pos-btn-lg">Complete Order - $45.99</button>
```

### POS Terminal Layout

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

### Cart Item

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

---

## Code Conventions

### HTML/Jinja2

- Semantic elements: `<nav>`, `<main>`, `<aside>`, `<button>`
- Include `lang` attribute on `<html>`
- Use `type="button"` on non-submit buttons
- Use `data-*` attributes for JS hooks, not classes
- Use Jinja2 macros for reusable components

### CSS

- BEM-like: `.pos-component`, `.pos-component-element`, `.pos-component--modifier`
- Prefix all custom classes with `pos-`
- Use CSS custom properties for colors, spacing, typography
- Mobile-first media queries only
- No `!important` except for utility overrides

### JavaScript

- ES2022+ features (modules, optional chaining, nullish coalescing)
- `const` by default, `let` when reassignment needed, never `var`
- Strict equality (`===`) always
- JSDoc comments for public APIs
- No global variables (use modules)

### File Naming

- Templates: `kebab-case.html`
- CSS: `kebab-case.css`
- JS: `kebab-case.js`
- JS Classes: `PascalCase` in code

---

## Browser Support

Chrome, Firefox, Safari, Edge (last 2 versions), iOS Safari, Chrome Android. No IE11.

---

## Design References

Reference Square POS, Clover, Lightspeed for patterns:
- Large, easily tappable buttons
- Minimal steps for common tasks
- Clear visual feedback
- Logical information hierarchy
- Quick access to frequent functions
