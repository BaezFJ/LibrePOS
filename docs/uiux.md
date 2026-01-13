# LibrePOS UI/UX - Project Guidelines

## Project Overview

LibrePOS is a modern, professional Point of Sale (POS) system UI/UX designed specifically for restaurant operations. This is a **pure frontend project** with no backend dependencies, focusing on creating a polished, production-ready interface that rivals industry leaders.

### Core Philosophy

- **Mobile & Touch First**: Every component designed for touch interaction before mouse/keyboard
- **Restaurant-Optimized**: UI patterns tailored for fast-paced restaurant environments
- **Accessibility First**: WCAG 2.1 AA compliance is mandatory, not optional
- **Performance Obsessed**: Sub-second interactions, instant feedback, zero jank

---

## Tech Stack

| Technology         | Version  | Purpose |
|--------------------|----------|---------|
| Materialize CSS    | 2.2.2    | CSS framework, grid system, components |
| Vanilla JavaScript | ES2022+  | All interactivity, no frameworks |
| HTML5              | Semantic | Structure and accessibility |
| CSS3               | Modern   | Custom properties, Grid, Flexbox |

### What We DON'T Use

- No jQuery
- No React/Vue/Angular
- No CSS preprocessors in production (vanilla CSS custom properties)
- No backend/server dependencies
- No external API calls for core functionality

---

## Project Structure

```
LibrePOS-UIUX/
├── css/
│   ├── vendor/
│   │   └── bootstrap.min.css      # Bootstrap 5.3.8
│   ├── style.css                  # Main stylesheet (development)
│   ├── style.min.css              # Minified stylesheet (production)
│   ├── themes/
│   │   ├── light.css              # Light theme variables
│   │   └── dark.css               # Dark theme variables
│   └── components/                # Component-specific styles
├── js/
│   ├── vendor/
│   │   └── bootstrap.min.js       # Bootstrap JS
│   ├── app.js                     # Main application entry
│   ├── modules/                   # Feature modules
│   │   ├── pos/                   # POS terminal functionality
│   │   ├── menu/                  # Menu management
│   │   ├── orders/                # Order processing
│   │   └── theme/                 # Theme switching
│   └── utils/                     # Utility functions
├── img/                           # Images and icons
├── pages/                         # HTML pages
│   ├── pos-terminal.html          # Main POS interface
│   ├── menu-management.html       # Menu editor
│   ├── order-history.html         # Order tracking
│   └── settings.html              # Configuration
└── index.html                     # Entry point
```

---

## Design System

### Color Palette

Use CSS custom properties for all colors. Never hardcode color values.

```css
:root {
  /* Brand Colors */
  --pos-primary: #2563eb;
  --pos-primary-hover: #1d4ed8;
  --pos-secondary: #64748b;
  --pos-accent: #10b981;

  /* Semantic Colors */
  --pos-success: #22c55e;
  --pos-warning: #f59e0b;
  --pos-danger: #ef4444;
  --pos-info: #3b82f6;

  /* Surface Colors (theme-dependent) */
  --pos-bg-primary: #ffffff;
  --pos-bg-secondary: #f8fafc;
  --pos-bg-tertiary: #f1f5f9;
  --pos-text-primary: #0f172a;
  --pos-text-secondary: #475569;
  --pos-border: #e2e8f0;
}

[data-theme="dark"] {
  --pos-bg-primary: #0f172a;
  --pos-bg-secondary: #1e293b;
  --pos-bg-tertiary: #334155;
  --pos-text-primary: #f8fafc;
  --pos-text-secondary: #94a3b8;
  --pos-border: #334155;
}
```

### Typography

```css
:root {
  /* Font Stack - System fonts for performance */
  --pos-font-family: system-ui, -apple-system, BlinkMacSystemFont,
                     'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  --pos-font-mono: ui-monospace, 'SF Mono', Monaco, 'Cascadia Code', monospace;

  /* Font Sizes - Touch-optimized minimums */
  --pos-text-xs: 0.75rem;    /* 12px - minimum for labels */
  --pos-text-sm: 0.875rem;   /* 14px */
  --pos-text-base: 1rem;     /* 16px - body text minimum */
  --pos-text-lg: 1.125rem;   /* 18px */
  --pos-text-xl: 1.25rem;    /* 20px */
  --pos-text-2xl: 1.5rem;    /* 24px */
  --pos-text-3xl: 1.875rem;  /* 30px */
  --pos-text-4xl: 2.25rem;   /* 36px - large displays */
}
```

### Icons (Material Symbols Rounded)

Use Google Material Symbols Rounded for all icons. Include via the variable font for flexibility in weight, fill, and optical size.

```html
<!-- Include in <head> -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap" rel="stylesheet">
```

```css
/* Icon base styles */
.material-symbols-rounded {
  font-size: 24px;
  line-height: 1;
  vertical-align: middle;
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
}

/* Filled icon variant */
.material-symbols-rounded.filled {
  font-variation-settings:
    'FILL' 1,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
}

/* Size variants */
.pos-icon-sm { font-size: 20px; font-variation-settings: 'opsz' 20; }
.pos-icon-lg { font-size: 32px; font-variation-settings: 'opsz' 32; }
.pos-icon-xl { font-size: 48px; font-variation-settings: 'opsz' 48; }
```

```html
<!-- Usage examples -->
<span class="material-symbols-rounded" aria-hidden="true">shopping_cart</span>
<span class="material-symbols-rounded filled" aria-hidden="true">favorite</span>
<span class="material-symbols-rounded pos-icon-lg" aria-hidden="true">receipt_long</span>
```

### Spacing Scale

```css
:root {
  --pos-space-1: 0.25rem;   /* 4px */
  --pos-space-2: 0.5rem;    /* 8px */
  --pos-space-3: 0.75rem;   /* 12px */
  --pos-space-4: 1rem;      /* 16px */
  --pos-space-5: 1.25rem;   /* 20px */
  --pos-space-6: 1.5rem;    /* 24px */
  --pos-space-8: 2rem;      /* 32px */
  --pos-space-10: 2.5rem;   /* 40px */
  --pos-space-12: 3rem;     /* 48px */
}
```

---

## Touch & Mobile First Guidelines

### Minimum Touch Target Sizes

All interactive elements MUST meet these minimum sizes:

```css
/* Minimum touch target: 44x44px (WCAG 2.1 AAA) */
/* Recommended touch target: 48x48px */

.pos-btn {
  min-height: 48px;
  min-width: 48px;
  padding: var(--pos-space-3) var(--pos-space-4);
}

.pos-menu-item {
  min-height: 56px;  /* Larger for frequent taps */
  padding: var(--pos-space-4);
}

/* Touch spacing between targets */
.pos-btn + .pos-btn {
  margin-left: var(--pos-space-2);  /* 8px minimum gap */
}
```

### Touch Interaction Patterns

```javascript
// Always use pointer events for cross-device compatibility
element.addEventListener('pointerdown', handleInteraction);
element.addEventListener('pointerup', handleInteraction);

// Provide immediate visual feedback
element.addEventListener('pointerdown', () => {
  element.classList.add('pos-active');
});

// Remove feedback on pointer up or leave
element.addEventListener('pointerup', () => {
  element.classList.remove('pos-active');
});
element.addEventListener('pointerleave', () => {
  element.classList.remove('pos-active');
});
```

### Responsive Breakpoints

```css
/* Mobile First - Base styles are for mobile */

/* Tablet Portrait */
@media (min-width: 768px) { }

/* Tablet Landscape / Small Desktop */
@media (min-width: 1024px) { }

/* Desktop */
@media (min-width: 1280px) { }

/* Large Desktop / POS Terminal Displays */
@media (min-width: 1536px) { }
```

### Device-Specific Considerations

```css
/* Prevent text selection on touch devices for interactive elements */
.pos-interactive {
  -webkit-user-select: none;
  user-select: none;
  -webkit-touch-callout: none;
}

/* Prevent pull-to-refresh on mobile */
body {
  overscroll-behavior: none;
}

/* Remove tap highlight on mobile WebKit */
.pos-btn {
  -webkit-tap-highlight-color: transparent;
}
```

---

## Dual Theme System

### Theme Toggle Implementation

```html
<!-- Theme toggle button -->
<button
  type="button"
  class="pos-btn pos-btn-icon"
  id="theme-toggle"
  aria-label="Toggle dark mode"
  aria-pressed="false">
  <span class="material-symbols-rounded pos-icon-light" aria-hidden="true">light_mode</span>
  <span class="material-symbols-rounded pos-icon-dark" aria-hidden="true">dark_mode</span>
</button>
```

```javascript
// Theme management module
const ThemeManager = {
  STORAGE_KEY: 'pos-theme',

  init() {
    const savedTheme = localStorage.getItem(this.STORAGE_KEY);
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = savedTheme || (prefersDark ? 'dark' : 'light');
    this.setTheme(theme);

    // Listen for system preference changes
    window.matchMedia('(prefers-color-scheme: dark)')
      .addEventListener('change', (e) => {
        if (!localStorage.getItem(this.STORAGE_KEY)) {
          this.setTheme(e.matches ? 'dark' : 'light');
        }
      });
  },

  setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(this.STORAGE_KEY, theme);

    // Update meta theme-color for browser chrome
    const metaTheme = document.querySelector('meta[name="theme-color"]');
    metaTheme?.setAttribute('content', theme === 'dark' ? '#0f172a' : '#ffffff');
  },

  toggle() {
    const current = document.documentElement.getAttribute('data-theme');
    this.setTheme(current === 'dark' ? 'light' : 'dark');
  }
};
```

### Theme-Aware Component Example

```css
/* Button that adapts to theme */
.pos-btn-primary {
  background-color: var(--pos-primary);
  color: #ffffff;
  border: none;
  transition: background-color 0.15s ease;
}

.pos-btn-primary:hover,
.pos-btn-primary:focus-visible {
  background-color: var(--pos-primary-hover);
}

/* Surface cards */
.pos-card {
  background-color: var(--pos-bg-secondary);
  border: 1px solid var(--pos-border);
  border-radius: var(--pos-space-2);
}
```

---

## Accessibility Requirements (WCAG 2.1 AA)

### Mandatory Checklist

- [ ] **Color Contrast**: Minimum 4.5:1 for normal text, 3:1 for large text
- [ ] **Focus Indicators**: Visible focus rings on all interactive elements
- [ ] **Keyboard Navigation**: All functionality accessible via keyboard
- [ ] **Touch Targets**: Minimum 44x44px for all interactive elements
- [ ] **Screen Reader Support**: Proper ARIA labels and live regions
- [ ] **Reduced Motion**: Respect `prefers-reduced-motion`
- [ ] **Error Identification**: Clear error messages with suggestions

### Focus Management

```css
/* Custom focus ring - visible and accessible */
.pos-focus-ring:focus-visible {
  outline: 3px solid var(--pos-primary);
  outline-offset: 2px;
}

/* Remove default outline when using custom */
.pos-focus-ring:focus {
  outline: none;
}
```

### ARIA Patterns

```html
<!-- Live region for order updates -->
<div
  role="status"
  aria-live="polite"
  aria-label="Order status updates"
  class="pos-sr-only"
  id="order-status">
</div>

<!-- Menu item button with state -->
<button
  type="button"
  class="pos-menu-item"
  aria-pressed="false"
  aria-describedby="item-price-123">
  <span class="pos-menu-item-name">Caesar Salad</span>
  <span class="pos-menu-item-price" id="item-price-123">$12.99</span>
</button>

<!-- Modal dialog -->
<dialog
  class="pos-modal"
  aria-labelledby="modal-title"
  aria-describedby="modal-desc">
  <h2 id="modal-title">Confirm Order</h2>
  <p id="modal-desc">Are you ready to submit this order?</p>
</dialog>
```

### Screen Reader Utilities

```css
/* Visually hidden but accessible to screen readers */
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

/* Show on focus for skip links */
.pos-sr-only-focusable:focus {
  position: static;
  width: auto;
  height: auto;
  margin: 0;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## Performance Guidelines

### Critical Metrics

| Metric | Target |
|--------|--------|
| First Contentful Paint | < 1.0s |
| Largest Contentful Paint | < 1.5s |
| Time to Interactive | < 2.0s |
| Cumulative Layout Shift | < 0.1 |
| Total Bundle Size (JS) | < 100KB gzipped |
| Total Bundle Size (CSS) | < 50KB gzipped |

### JavaScript Best Practices

```javascript
// Use event delegation for dynamic content
document.getElementById('menu-grid').addEventListener('click', (e) => {
  const menuItem = e.target.closest('.pos-menu-item');
  if (menuItem) {
    handleMenuItemClick(menuItem);
  }
});

// Debounce expensive operations
function debounce(fn, delay = 150) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

// Use requestAnimationFrame for visual updates
function updateCartDisplay(items) {
  requestAnimationFrame(() => {
    renderCartItems(items);
  });
}

// Lazy load non-critical modules
async function loadReportModule() {
  const { ReportManager } = await import('./modules/reports/index.js');
  return new ReportManager();
}
```

### CSS Performance

```css
/* Avoid expensive selectors */
/* Bad: */ .pos-grid > * > .pos-item { }
/* Good: */ .pos-grid-item { }

/* Use will-change sparingly and only when needed */
.pos-modal.is-animating {
  will-change: transform, opacity;
}

/* Prefer transform/opacity for animations */
.pos-slide-in {
  transform: translateX(100%);
  transition: transform 0.3s ease-out;
}
.pos-slide-in.is-visible {
  transform: translateX(0);
}

/* Contain paint for isolated components */
.pos-cart-panel {
  contain: layout paint;
}
```

### Asset Optimization

- **Images**: Use WebP with PNG/JPG fallbacks, implement lazy loading
- **Icons**: Use Google Material Symbols Rounded via the variable font for optimal flexibility and performance
- **Fonts**: System font stack for text; Google Material Symbols Rounded for icons

---

## Component Patterns

### Button Variants

```html
<!-- Primary action -->
<button type="button" class="pos-btn pos-btn-primary">
  Add to Order
</button>

<!-- Secondary action -->
<button type="button" class="pos-btn pos-btn-secondary">
  Cancel
</button>

<!-- Danger/destructive action -->
<button type="button" class="pos-btn pos-btn-danger">
  Void Item
</button>

<!-- Icon button with label -->
<button type="button" class="pos-btn pos-btn-icon" aria-label="Print receipt">
  <span class="material-symbols-rounded" aria-hidden="true">print</span>
</button>

<!-- Large touch-optimized button -->
<button type="button" class="pos-btn pos-btn-primary pos-btn-lg">
  Complete Order - $45.99
</button>
```

### POS Terminal Layout

```html
<div class="pos-terminal">
  <!-- Left: Menu Items -->
  <main class="pos-menu-panel" role="main">
    <nav class="pos-category-nav" aria-label="Menu categories">
      <!-- Category tabs -->
    </nav>
    <div class="pos-menu-grid" role="list" aria-label="Menu items">
      <!-- Menu item buttons -->
    </div>
  </main>

  <!-- Right: Order/Cart -->
  <aside class="pos-cart-panel" aria-label="Current order">
    <header class="pos-cart-header">
      <h2>Current Order</h2>
    </header>
    <ul class="pos-cart-items" aria-label="Order items">
      <!-- Cart items -->
    </ul>
    <footer class="pos-cart-footer">
      <div class="pos-cart-total" aria-live="polite">
        Total: <strong>$45.99</strong>
      </div>
      <button type="button" class="pos-btn pos-btn-primary pos-btn-lg">
        Pay Now
      </button>
    </footer>
  </aside>
</div>
```

### Order Item Component

```html
<li class="pos-cart-item">
  <div class="pos-cart-item-info">
    <span class="pos-cart-item-qty">2x</span>
    <span class="pos-cart-item-name">Caesar Salad</span>
    <span class="pos-cart-item-mods">No croutons, dressing on side</span>
  </div>
  <div class="pos-cart-item-actions">
    <span class="pos-cart-item-price">$25.98</span>
    <button
      type="button"
      class="pos-btn pos-btn-icon pos-btn-sm"
      aria-label="Edit Caesar Salad">
      <span class="material-symbols-rounded" aria-hidden="true">edit</span>
    </button>
    <button
      type="button"
      class="pos-btn pos-btn-icon pos-btn-sm pos-btn-danger"
      aria-label="Remove Caesar Salad from order">
      <span class="material-symbols-rounded" aria-hidden="true">delete</span>
    </button>
  </div>
</li>
```

---

## JavaScript Module Structure

### Module Pattern

```javascript
// modules/pos/cart.js
export const Cart = {
  items: [],

  init() {
    this.bindEvents();
    this.render();
  },

  bindEvents() {
    document.getElementById('menu-grid')
      .addEventListener('click', this.handleMenuClick.bind(this));
  },

  addItem(item) {
    const existing = this.items.find(i => i.id === item.id);
    if (existing) {
      existing.quantity += 1;
    } else {
      this.items.push({ ...item, quantity: 1 });
    }
    this.render();
    this.announceUpdate(`${item.name} added to order`);
  },

  removeItem(itemId) {
    const item = this.items.find(i => i.id === itemId);
    this.items = this.items.filter(i => i.id !== itemId);
    this.render();
    if (item) {
      this.announceUpdate(`${item.name} removed from order`);
    }
  },

  getTotal() {
    return this.items.reduce((sum, item) => {
      return sum + (item.price * item.quantity);
    }, 0);
  },

  render() {
    requestAnimationFrame(() => {
      // Render cart items
    });
  },

  // Screen reader announcement
  announceUpdate(message) {
    const status = document.getElementById('order-status');
    if (status) {
      status.textContent = message;
    }
  }
};
```

### App Initialization

```javascript
// js/app.js
import { ThemeManager } from './modules/theme/index.js';
import { Cart } from './modules/pos/cart.js';
import { MenuGrid } from './modules/pos/menu.js';

const App = {
  async init() {
    // Initialize theme first (prevents flash)
    ThemeManager.init();

    // Initialize core modules
    Cart.init();
    MenuGrid.init();

    // Register service worker for offline support (optional)
    if ('serviceWorker' in navigator) {
      await navigator.serviceWorker.register('/sw.js');
    }
  }
};

// Start app when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => App.init());
} else {
  App.init();
}
```

---

## Code Style & Conventions

### HTML

- Use semantic elements (`<nav>`, `<main>`, `<aside>`, `<button>`, etc.)
- Always include `lang` attribute on `<html>`
- Use `type="button"` on non-submit buttons
- Include proper `aria-*` attributes for dynamic content
- Use `data-*` attributes for JavaScript hooks, not classes

### CSS

- Use BEM-like naming: `.pos-component`, `.pos-component-element`, `.pos-component--modifier`
- Prefix all custom classes with `pos-` to avoid Bootstrap conflicts
- Use CSS custom properties for all colors, spacing, and typography
- Mobile-first media queries only
- No `!important` except for utility overrides

### JavaScript

- ES2022+ features (modules, optional chaining, nullish coalescing)
- Use `const` by default, `let` when reassignment needed, never `var`
- Strict equality (`===`) always
- Descriptive function and variable names
- JSDoc comments for public APIs
- No global variables (use modules)

### File Naming

- HTML: `kebab-case.html` (e.g., `pos-terminal.html`)
- CSS: `kebab-case.css` (e.g., `pos-components.css`)
- JS: `kebab-case.js` (e.g., `cart-manager.js`)
- JS Classes/Modules: `PascalCase` in code (e.g., `CartManager`)

---

## Development Commands

```bash
# Install dependencies
npm install

# Start development server with hot reload
npm start

# Build for production
npm run build

# Run tests (when configured)
npm test
```

---

## Browser Support

| Browser | Version |
|---------|---------|
| Chrome | Last 2 versions |
| Firefox | Last 2 versions |
| Safari | Last 2 versions |
| Edge | Last 2 versions |
| iOS Safari | Last 2 versions |
| Chrome Android | Last 2 versions |

**Note**: This is a modern browsers only project. No IE11 support.

---

## Design Inspiration References

When implementing UI patterns, reference these industry leaders:

- **Square POS**: Clean grid layouts, prominent action buttons, intuitive category navigation
- **Clover**: Card-based item display, clear visual hierarchy, efficient order management
- **Lightspeed**: Professional aesthetics, data-dense layouts, comprehensive modifier systems

Focus on what makes these systems efficient for high-volume restaurant operations:
- Large, easily tappable buttons
- Minimal steps to complete common tasks
- Clear visual feedback for all actions
- Logical information hierarchy
- Quick access to frequently used functions

---

## Quick Reference

### Common Tasks

| Task | Implementation |
|------|----------------|
| Add theme support | Use `var(--pos-*)` custom properties |
| Make touchable | Min 48x48px, use `pointerdown`/`pointerup` |
| Add to screen reader | Use `aria-label`, `aria-live`, `role` |
| Animate safely | Use `transform`/`opacity`, check `prefers-reduced-motion` |
| Handle state | Use `data-*` attributes and `aria-*` states |

### CSS Class Prefixes

| Prefix | Purpose |
|--------|---------|
| `.pos-` | All LibrePOS components |
| `.pos-btn-` | Button variants |
| `.pos-card-` | Card components |
| `.pos-menu-` | Menu-related components |
| `.pos-cart-` | Cart/order components |
| `.pos-modal-` | Modal dialogs |
| `.pos-sr-` | Screen reader utilities |
