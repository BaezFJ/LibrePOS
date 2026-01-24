# LibrePOS UI/UX Guidelines

> Modern POS system built with Flask, Jinja2, Materialize CSS 2.2.2, and vanilla JavaScript (ES2022+)

---

## Core Principles

- **Mobile & Touch First**: Design for touch before mouse/keyboard
- **Restaurant-Optimized**: Fast-paced environment patterns
- **Accessibility First**: WCAG 2.1 AA mandatory
- **Performance Obsessed**: Sub-second interactions

---

## Quick Reference

| Task | Implementation |
|------|----------------|
| Add button | Use `.btn .filled/.tonal/.outlined/.text` (Materialize) |
| Add card | Use `.card`, `.card-content`, `.card-action` (Materialize) |
| Add modal | Use `.modal`, `.modal-content`, `.modal-footer` (Materialize) |
| Add theme support | Use `var(--pos-*)` or `var(--md-sys-color-*)` custom properties |
| Make touchable | Min 48x48px, use `pointerdown`/`pointerup` |
| Add to screen reader | Use `aria-label`, `aria-live`, `role` |
| Animate safely | Use `transform`/`opacity`, check `prefers-reduced-motion` |
| Handle state | Use `data-*` attributes and `aria-*` states |
| Add icon | `<span class="material-symbols-rounded" aria-hidden="true">icon_name</span>` |

---

## CSS Files

| File | Purpose |
|------|---------|
| `variables.css` | Design tokens (MaterializeCSS colors, spacing, typography) |
| `main.css` | Global layout, navigation, components |
| `utilities.css` | Utility classes (flexbox, colors) |
| `override.css` | Materialize CSS overrides |

---

## CSS Strategy: Materialize First

| Priority | Classes | Usage |
|----------|---------|-------|
| 1st | Materialize CSS | Buttons, cards, modals, forms, grids |
| 2nd | Utility classes | Flex helpers, color utilities (no prefix) |
| 3rd | `.pos-*` custom | POS-specific components only |

### Custom `.pos-*` Components (Only These)

| Component | Classes | Purpose |
|-----------|---------|---------|
| Terminal layout | `.pos-terminal`, `.pos-menu-panel`, `.pos-cart-panel` | Split-screen POS |
| Cart | `.pos-cart-*`, `.pos-cart-item-*` | Order cart components |
| Accessibility | `.pos-sr-only` | Screen reader utilities |
| Placeholder states | `.placeholder-*` | Empty state UI |
| Action bar | `.action-bar-*` | Floating toolbar |

---

## Key Standards

### Touch Targets

| Size | Usage |
|------|-------|
| 44x44px | Minimum (WCAG) |
| 48x48px | Recommended |
| 56px | Menu items |
| 8px gap | Between targets |

### Performance Targets

| Metric | Target |
|--------|--------|
| First Contentful Paint | < 1.0s |
| Time to Interactive | < 2.0s |
| JS Bundle (gzipped) | < 100KB |

### Accessibility

| Requirement | Standard |
|-------------|----------|
| Color Contrast | 4.5:1 text |
| Focus Indicators | Visible rings |
| Touch Targets | 44x44px min |

---

## Theme System

```javascript
// Set theme
document.documentElement.setAttribute('data-theme', 'dark');
localStorage.setItem('pos-theme', 'dark');
```

Light theme: MaterializeCSS default | Dark theme: MaterializeCSS dark

---

## Design References

Reference Square POS, Clover, Lightspeed for patterns:
- Large, easily tappable buttons
- Minimal steps for common tasks
- Clear visual feedback
- Logical information hierarchy

---

## Browser Support

Chrome, Firefox, Safari, Edge (last 2 versions), iOS Safari, Chrome Android. No IE11.

---

## Detailed Documentation

- [Design System](uiux/design-system.md) - Colors, typography, spacing, icons
- [Accessibility](uiux/accessibility.md) - WCAG compliance, ARIA patterns
- [Touch & Responsive](uiux/touch-responsive.md) - Touch targets, breakpoints
- [Performance](uiux/performance.md) - Targets, JS/CSS optimization
- [Components](uiux/components.md) - Button patterns, layouts
- [Conventions](uiux/conventions.md) - HTML, CSS, JS standards
