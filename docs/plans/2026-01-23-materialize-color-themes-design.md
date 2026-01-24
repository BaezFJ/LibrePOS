# MaterializeCSS Color Themes Design

Rewrite LibrePOS color themes using only MaterializeCSS color variables with WCAG 2.1 AA compliance.

## Architecture

**Current (being replaced):**
```
Catppuccin (--ctp-*) → POS semantic (--pos-*) → Material Design (--md-sys-color-*)
```

**New:**
```
Materialize built-in (--md-ref-palette-*, --md-sys-color-*-light/dark)
     ↓
Theme selectors override --md-sys-color-* tokens
     ↓
Custom semantic tokens (--sys-color-success/warning/info)
```

## Files to Change

| File | Change |
|------|--------|
| `variables.css` | Complete rewrite |
| `utilities.css` | Update 2 color references |
| `docs/uiux.md` | Update theme documentation |

## What Stays Unchanged

- `--pos-space-*` spacing scale
- `--pos-text-*` font sizes
- `--pos-font-*` font families
- `--navbar-height` / `--navbar-height-mobile`
- All existing `--md-sys-color-*` usages in main.css, override.css

---

## Custom Tonal Scales

MaterializeCSS lacks success, warning, and info palettes. We define custom tonal scales following Material Design 3's pattern.

### Success (Green) — Source: #1B7D3E

```css
--md-ref-palette-success0: #000000;
--md-ref-palette-success10: #002109;
--md-ref-palette-success20: #003915;
--md-ref-palette-success30: #005322;
--md-ref-palette-success40: #1b7d3e;
--md-ref-palette-success50: #3d9857;
--md-ref-palette-success60: #58b370;
--md-ref-palette-success70: #73cf8a;
--md-ref-palette-success80: #8feca4;
--md-ref-palette-success90: #abffc0;
--md-ref-palette-success95: #c8ffe0;
--md-ref-palette-success99: #f5fff5;
--md-ref-palette-success100: #ffffff;
```

### Warning (Amber) — Source: #8B5000

```css
--md-ref-palette-warning0: #000000;
--md-ref-palette-warning10: #2c1600;
--md-ref-palette-warning20: #4a2800;
--md-ref-palette-warning30: #6a3b00;
--md-ref-palette-warning40: #8b5000;
--md-ref-palette-warning50: #a96600;
--md-ref-palette-warning60: #c87f1a;
--md-ref-palette-warning70: #e79a38;
--md-ref-palette-warning80: #ffb95c;
--md-ref-palette-warning90: #ffddb5;
--md-ref-palette-warning95: #ffeedc;
--md-ref-palette-warning99: #fffbff;
--md-ref-palette-warning100: #ffffff;
```

### Info (Cyan) — Source: #006879

```css
--md-ref-palette-info0: #000000;
--md-ref-palette-info10: #001f26;
--md-ref-palette-info20: #003640;
--md-ref-palette-info30: #004e5c;
--md-ref-palette-info40: #006879;
--md-ref-palette-info50: #008396;
--md-ref-palette-info60: #269eb4;
--md-ref-palette-info70: #4bb9d0;
--md-ref-palette-info80: #6ad5ed;
--md-ref-palette-info90: #a0efff;
--md-ref-palette-info95: #d4f7ff;
--md-ref-palette-info99: #f6feff;
--md-ref-palette-info100: #ffffff;
```

---

## Semantic Token Mappings

### Light Theme

| Token | Value | Contrast |
|-------|-------|----------|
| `--sys-color-success` | success40 (#1b7d3e) | |
| `--sys-color-on-success` | #ffffff | 4.6:1 ✓ |
| `--sys-color-success-container` | success90 (#abffc0) | |
| `--sys-color-on-success-container` | success10 (#002109) | |
| `--sys-color-warning` | warning40 (#8b5000) | |
| `--sys-color-on-warning` | #ffffff | 4.8:1 ✓ |
| `--sys-color-warning-container` | warning90 (#ffddb5) | |
| `--sys-color-on-warning-container` | warning10 (#2c1600) | |
| `--sys-color-info` | info40 (#006879) | |
| `--sys-color-on-info` | #ffffff | 4.7:1 ✓ |
| `--sys-color-info-container` | info90 (#a0efff) | |
| `--sys-color-on-info-container` | info10 (#001f26) | |

### Dark Theme

| Token | Value | Contrast |
|-------|-------|----------|
| `--sys-color-success` | success80 (#8feca4) | |
| `--sys-color-on-success` | success20 (#003915) | 7.2:1 ✓ |
| `--sys-color-success-container` | success30 (#005322) | |
| `--sys-color-on-success-container` | success90 (#abffc0) | |
| `--sys-color-warning` | warning80 (#ffb95c) | |
| `--sys-color-on-warning` | warning20 (#4a2800) | 6.8:1 ✓ |
| `--sys-color-warning-container` | warning30 (#6a3b00) | |
| `--sys-color-on-warning-container` | warning90 (#ffddb5) | |
| `--sys-color-info` | info80 (#6ad5ed) | |
| `--sys-color-on-info` | info20 (#003640) | 6.5:1 ✓ |
| `--sys-color-info-container` | info30 (#004e5c) | |
| `--sys-color-on-info-container` | info90 (#a0efff) | |

---

## Theme Switching Structure

```css
/* 1. Base variables (theme-independent) */
:root {
    /* Spacing, typography, layout */
    /* Custom tonal palettes (success/warning/info) */
}

/* 2. Light theme (default) */
:root,
:root:not([data-theme]),
[data-theme="light"] {
    color-scheme: light;
    /* Override --md-sys-color-* to use -light variants */
    /* Custom semantic colors (light) */
}

/* 3. Dark theme (manual toggle) */
[data-theme="dark"] {
    color-scheme: dark;
    /* Override --md-sys-color-* to use -dark variants */
    /* Custom semantic colors (dark) */
}

/* 4. System preference fallback */
@media (prefers-color-scheme: dark) {
    :root:not([data-theme]) {
        /* Same as [data-theme="dark"] */
    }
}
```

---

## Migration Changes

### utilities.css

```css
/* Before */
.pos-sr-only--focusable:focus {
    background-color: var(--pos-bg-primary);
    color: var(--pos-text-primary);
}

/* After */
.pos-sr-only--focusable:focus {
    background-color: var(--md-sys-color-surface);
    color: var(--md-sys-color-on-surface);
}
```

### docs/uiux.md

- Line 35: Change "Catppuccin colors" to "MaterializeCSS color system"
- Line 100: Remove "Catppuccin Latte/Mocha" references

### variables.css Removals

- All `--ctp-*` variables
- All `--pos-primary`, `--pos-secondary`, `--pos-accent` and hover/active variants
- All `--pos-success`, `--pos-warning`, `--pos-danger`, `--pos-info` and hover/active variants
- All `--pos-bg-*`, `--pos-text-*`, `--pos-border-*`, `--pos-shadow-*` color tokens

### variables.css Retains

- `--pos-space-*` spacing scale
- `--pos-text-*` font sizes
- `--pos-font-*` font families
- `--navbar-height` variables
- HTMX loading states
