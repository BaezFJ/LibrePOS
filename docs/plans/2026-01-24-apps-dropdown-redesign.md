# Apps Dropdown Redesign

## Overview

Update the apps-dropdown component styling to match the reference design with improved visual hierarchy, spacing, and a "View all" footer action.

## Approach

CSS-only update with minimal HTML changes. Leverages existing component structure.

## Files to Modify

1. `librepos/app/static/css/main.css` - Update component styles
2. `librepos/app/static/css/main.min.css` - Minified version
3. `librepos/app/templates/layouts/admin.html` - Add footer link

## Design Specifications

### Container & Header

```css
.dropdown-content.apps-dropdown {
    padding: 16px;
    width: 320px;
    border-radius: 12px;
}

.apps-dropdown-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 4px 16px;
}
```

### Grid & Tiles

```css
.apps-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--pos-space-3);  /* 12px */
}

.app-tile {
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: var(--pos-space-2);
    min-height: 88px;
    padding: var(--pos-space-3);
    border-radius: 12px;
    border: 1px solid var(--md-sys-color-outline-variant);
    background: var(--md-sys-color-surface);
    text-decoration: none;
    transition: background-color 0.15s ease, border-color 0.15s ease;
}

.app-tile:hover {
    background: var(--md-sys-color-surface-variant);
    border-color: var(--md-sys-color-outline);
}
```

### Footer

```css
.apps-dropdown-footer {
    margin-top: var(--pos-space-4);
    padding-top: var(--pos-space-3);
    border-top: 1px solid var(--md-sys-color-outline-variant);
}

.apps-dropdown-footer a {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--pos-space-2);
    width: 100%;
    padding: var(--pos-space-3) var(--pos-space-4);
    border-radius: 12px;
    background: var(--md-sys-color-surface);
    border: 1px solid var(--md-sys-color-outline-variant);
    color: var(--md-sys-color-on-surface);
    font-size: 0.875rem;
    font-weight: 500;
    text-decoration: none;
    transition: background-color 0.15s ease, border-color 0.15s ease;
}

.apps-dropdown-footer a:hover {
    background: var(--md-sys-color-surface-variant);
    border-color: var(--md-sys-color-outline);
}
```

### HTML Addition (admin.html)

Add after `.apps-grid` div, inside `.apps-dropdown`:

```html
<div class="apps-dropdown-footer">
    <a href="#!">
        <span class="material-symbols-rounded" aria-hidden="true">grid_view</span>
        View all
    </a>
</div>
```

## Implementation Steps

1. Update `.dropdown-content.apps-dropdown` styles in `main.css`
2. Update `.apps-dropdown-header` padding
3. Update `.apps-grid` gap
4. Update `.app-tile` styles (height, radius, colors, transitions)
5. Add `.apps-dropdown-footer` and link styles
6. Add footer HTML to `admin.html`
7. Minify CSS to `main.min.css`

## Accessibility

- Footer link includes icon with `aria-hidden="true"`
- Touch targets meet 48x48px minimum (tiles are 88px+ tall)
- Color contrast maintained via existing design system variables
- Focus states inherited from existing button/link styles
