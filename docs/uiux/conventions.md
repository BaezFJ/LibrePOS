# Code Conventions

> HTML, CSS, and JavaScript standards

---

## HTML/Jinja2

- Semantic elements: `<nav>`, `<main>`, `<aside>`, `<button>`
- Include `lang` attribute on `<html>`
- Use `type="button"` on non-submit buttons
- Use `data-*` attributes for JS hooks, not classes
- Use Jinja2 macros for reusable components

---

## CSS

### Strategy: Materialize First

1. **Use Materialize CSS classes** for standard components
2. **Use utility classes** without prefix for layout helpers
3. **Use `.pos-*` prefix** ONLY for POS-specific components

### Naming

| Type | Prefix | Example |
|------|--------|---------|
| Materialize | None | `.btn`, `.card`, `.modal` |
| Utility | None | `.flex-row`, `.space-between` |
| POS-specific | `.pos-` | `.pos-terminal`, `.pos-cart-item` |

### CSS Custom Properties

- `var(--md-sys-color-*)` - Materialize theming tokens
- `var(--pos-*)` - LibrePOS spacing/typography
- `var(--ctp-*)` - Direct Catppuccin colors

### Rules

- Mobile-first media queries only
- No `!important` except utilities
- Override Materialize in `override.css`, not inline

---

## JavaScript

- ES2022+ features (modules, optional chaining, nullish coalescing)
- `const` by default, `let` when reassignment needed, never `var`
- Strict equality (`===`) always
- JSDoc comments for public APIs
- No global variables (use modules)

---

## File Naming

| Type | Convention |
|------|------------|
| Templates | `kebab-case.html` |
| CSS | `kebab-case.css` |
| JS | `kebab-case.js` |
| JS Classes | `PascalCase` in code |

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

## Browser Support

Chrome, Firefox, Safari, Edge (last 2 versions), iOS Safari, Chrome Android. No IE11.
