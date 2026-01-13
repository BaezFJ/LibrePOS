# LibrePOS UI/UX - Project Guidelines

## Project Overview

LibrePOS is a modern, professional Point of Sale (POS) system built with Flask for restaurant operations. The frontend uses Jinja2 templates with Materialize CSS, creating a polished, production-ready interface that rivals industry leaders.

### Core Philosophy

- **Mobile & Touch First**: Every component designed for touch interaction before mouse/keyboard
- **Restaurant-Optimized**: UI patterns tailored for fast-paced restaurant environments
- **Accessibility First**: WCAG 2.1 AA compliance is mandatory, not optional
- **Performance Obsessed**: Sub-second interactions, instant feedback, zero jank

---

## Tech Stack

| Technology         | Version  | Purpose |
|--------------------|----------|---------|
| Flask              | Latest   | Backend framework with factory pattern |
| Jinja2             | Latest   | Server-side templating |
| Materialize CSS    | 2.2.2    | CSS framework, grid system, components |
| Vanilla JavaScript | ES2022+  | All frontend interactivity, no frameworks |
| HTML5              | Semantic | Structure and accessibility |
| CSS3               | Modern   | Custom properties, Grid, Flexbox |

### What We DON'T Use

- No jQuery
- No React/Vue/Angular
- No CSS preprocessors in production (vanilla CSS custom properties)
- No external API calls for core functionality

---

## Project Structure

```
librepos/
├── app/
│   ├── __init__.py               # Application factory (create_app)
│   ├── config.py                 # Configuration classes
│   ├── extensions.py             # Flask extension instances
│   ├── blueprints/               # Feature blueprints
│   │   └── {blueprint}/
│   │       ├── __init__.py       # Blueprint registration
│   │       ├── routes.py         # HTTP route handlers
│   │       ├── models.py         # SQLAlchemy models
│   │       ├── services.py       # Business logic layer
│   │       ├── schemas.py        # Marshmallow schemas
│   │       ├── forms.py          # WTForms definitions
│   │       ├── static/           # Blueprint-specific assets
│   │       │   ├── css/
│   │       │   └── js/
│   │       └── templates/        # Blueprint-specific templates
│   │           └── {blueprint}/
│   ├── shared/                   # Decorators, helpers, validators
│   ├── static/                   # Global static assets
│   │   ├── vendor/               # Third-party libraries
│   │   │   ├── materialize/      # Materialize CSS & JS
│   │   │   ├── google/           # Material Symbols fonts
│   │   │   ├── chartjs/          # Chart.js
│   │   │   ├── sortablejs/       # SortableJS
│   │   │   └── interactjs/       # interact.js
│   │   ├── css/
│   │   │   ├── variables.css     # Design system tokens (Catppuccin)
│   │   │   ├── main.css          # Global styles
│   │   │   ├── utilities.css     # Utility classes
│   │   │   └── override.css      # Materialize overrides
│   │   ├── js/
│   │   │   ├── app.js            # Main application entry
│   │   │   ├── utils.js          # Utility functions
│   │   │   └── sw.js             # Service worker
│   │   └── img/                  # Images and icons
│   └── templates/                # Base templates
│       ├── base.html             # Master layout
│       ├── layouts/              # Page layouts (admin, pos, kds)
│       ├── components/           # Reusable Jinja2 components
│       ├── macros/               # Jinja2 macro libraries
│       └── errors/               # Error pages
├── migrations/                   # Flask-Migrate database migrations
├── tests/                        # Test suite
├── docs/                         # Documentation
└── scripts/                      # Utility scripts
```

---

## Design System

### Color Palette (Catppuccin)

The design system uses [Catppuccin](https://catppuccin.com/) color palette:
- **Light theme**: Catppuccin Latte
- **Dark theme**: Catppuccin Mocha

All colors are defined in `app/static/css/variables.css` using CSS custom properties.

```css
/* Light Theme - Catppuccin Latte */
:root, [data-theme="light"] {
  /* Brand Colors */
  --pos-primary: var(--ctp-blue);     /* #1e66f5 */
  --pos-secondary: var(--ctp-overlay0); /* #9ca0b0 */
  --pos-accent: var(--ctp-teal);      /* #179299 */

  /* Semantic Colors */
  --pos-success: var(--ctp-green);    /* #40a02b */
  --pos-warning: var(--ctp-yellow);   /* #df8e1d */
  --pos-danger: var(--ctp-red);       /* #d20f39 */
  --pos-info: var(--ctp-sapphire);    /* #209fb5 */

  /* Surface Colors */
  --pos-bg-primary: var(--ctp-base);    /* #eff1f5 */
  --pos-bg-secondary: var(--ctp-mantle); /* #e6e9ef */
  --pos-bg-tertiary: var(--ctp-surface0); /* #ccd0da */

  /* Text Colors */
  --pos-text-primary: var(--ctp-text);    /* #4c4f69 */
  --pos-text-secondary: var(--ctp-subtext1); /* #5c5f77 */
  --pos-text-muted: var(--ctp-subtext0);  /* #6c6f85 */

  /* Borders */
  --pos-border: var(--ctp-surface1);       /* #bcc0cc */
  --pos-border-strong: var(--ctp-surface2); /* #acb0be */
}

/* Dark Theme - Catppuccin Mocha */
[data-theme="dark"] {
  /* Brand Colors */
  --pos-primary: var(--ctp-blue);     /* #89b4fa */
  --pos-secondary: var(--ctp-overlay0); /* #6c7086 */
  --pos-accent: var(--ctp-teal);      /* #94e2d5 */

  /* Semantic Colors */
  --pos-success: var(--ctp-green);    /* #a6e3a1 */
  --pos-warning: var(--ctp-yellow);   /* #f9e2af */
  --pos-danger: var(--ctp-red);       /* #f38ba8 */
  --pos-info: var(--ctp-sapphire);    /* #74c7ec */

  /* Surface Colors */
  --pos-bg-primary: var(--ctp-base);    /* #1e1e2e */
  --pos-bg-secondary: var(--ctp-mantle); /* #181825 */
  --pos-bg-tertiary: var(--ctp-surface0); /* #313244 */

  /* Text Colors */
  --pos-text-primary: var(--ctp-text);    /* #cdd6f4 */
  --pos-text-secondary: var(--ctp-subtext1); /* #bac2de */
  --pos-text-muted: var(--ctp-subtext0);  /* #a6adc8 */

  /* Borders */
  --pos-border: var(--ctp-surface1);       /* #45475a */
  --pos-border-strong: var(--ctp-surface2); /* #585b70 */
}
```

### Additional Catppuccin Colors

The full Catppuccin palette is available via `--ctp-*` variables:

| Color | Latte | Mocha | Usage |
|-------|-------|-------|-------|
| rosewater | #dc8a78 | #f5e0dc | Decorative accents |
| flamingo | #dd7878 | #f2cdcd | Decorative accents |
| pink | #ea76cb | #f5c2e7 | Highlights |
| mauve | #8839ef | #cba6f7 | Links, special actions |
| maroon | #e64553 | #eba0ac | Alternative danger |
| peach | #fe640b | #fab387 | Attention, badges |
| sky | #04a5e5 | #89dceb | Alternative info |
| lavender | #7287fd | #b4befe | Focus states |

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

Use Google Material Symbols Rounded for all icons. The font is bundled locally in `app/static/vendor/google/`.

```html
<!-- Usage in Jinja2 templates -->
<span class="material-symbols-rounded" aria-hidden="true">shopping_cart</span>
<span class="material-symbols-rounded filled" aria-hidden="true">favorite</span>
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

    // Update meta theme-color for browser chrome (Catppuccin colors)
    const metaTheme = document.querySelector('meta[name="theme-color"]');
    metaTheme?.setAttribute('content', theme === 'dark' ? '#1e1e2e' : '#eff1f5');
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
  color: var(--md-sys-color-on-primary);
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
- **Icons**: Google Material Symbols Rounded bundled locally
- **Fonts**: System font stack for text; Material Symbols for icons
- **Vendor**: Materialize CSS, Chart.js, SortableJS, interact.js bundled locally

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

## Code Style & Conventions

### HTML / Jinja2

- Use semantic elements (`<nav>`, `<main>`, `<aside>`, `<button>`, etc.)
- Always include `lang` attribute on `<html>`
- Use `type="button"` on non-submit buttons
- Include proper `aria-*` attributes for dynamic content
- Use `data-*` attributes for JavaScript hooks, not classes
- Use Jinja2 macros for reusable components

### CSS

- Use BEM-like naming: `.pos-component`, `.pos-component-element`, `.pos-component--modifier`
- Prefix all custom classes with `pos-` to avoid Materialize conflicts
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

- Templates: `kebab-case.html` (e.g., `menu-list.html`)
- CSS: `kebab-case.css` (e.g., `pos-components.css`)
- JS: `kebab-case.js` (e.g., `cart-manager.js`)
- JS Classes/Modules: `PascalCase` in code (e.g., `CartManager`)

---

## Development Commands

```bash
# Run development server
flask run

# Database migrations
flask db migrate -m "description"
flask db upgrade

# Testing
pytest
pytest --cov=app

# Seed data
python scripts/seed_data.py
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

### CSS Files

| File | Purpose |
|------|---------|
| `variables.css` | Design tokens (Catppuccin colors, spacing, typography) |
| `main.css` | Global layout, navigation, components |
| `utilities.css` | Utility classes (flexbox, colors, etc.) |
| `override.css` | Materialize CSS overrides |
