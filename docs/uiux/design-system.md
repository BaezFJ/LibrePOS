# Design System

> Colors, typography, spacing, and icons

---

## Color Palette (Catppuccin)

All colors defined in `app/static/css/variables.css`. Light theme uses Catppuccin Latte, dark theme uses Catppuccin Mocha.

### Brand Colors

| Token | Light | Dark |
|-------|-------|------|
| `--pos-primary` | Blue `#1e66f5` | `#89b4fa` |
| `--pos-secondary` | Overlay `#9ca0b0` | `#6c7086` |
| `--pos-accent` | Teal `#179299` | `#94e2d5` |

### Semantic Colors

| Token | Purpose |
|-------|---------|
| `--pos-success` | Green - success states |
| `--pos-warning` | Yellow - warning states |
| `--pos-danger` | Red - error/destructive |
| `--pos-info` | Sapphire - informational |

### Surface Colors

| Token | Purpose |
|-------|---------|
| `--pos-bg-primary` | Base background |
| `--pos-bg-secondary` | Mantle (cards, panels) |
| `--pos-bg-tertiary` | Surface0 (elevated elements) |

### Text Colors

| Token | Purpose |
|-------|---------|
| `--pos-text-primary` | Main text |
| `--pos-text-secondary` | Secondary text |
| `--pos-text-muted` | Disabled/hint text |

### Borders

| Token | Purpose |
|-------|---------|
| `--pos-border` | Default border |
| `--pos-border-strong` | Emphasized border |

### Additional Catppuccin Colors

Available via `--ctp-*` variables: rosewater, flamingo, pink, mauve, maroon, peach, sky, lavender.

---

## Typography

```css
--pos-font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--pos-font-mono: ui-monospace, 'SF Mono', Monaco, 'Cascadia Code', monospace;
```

### Sizes

| Token | Size | Usage |
|-------|------|-------|
| `--pos-text-xs` | 0.75rem (12px) | Minimum for labels |
| `--pos-text-sm` | 0.875rem (14px) | Small text |
| `--pos-text-base` | 1rem (16px) | Body text minimum |
| `--pos-text-lg` | 1.125rem (18px) | Large text |
| `--pos-text-xl` | 1.25rem (20px) | Headings |
| `--pos-text-2xl` | 1.5rem (24px) | Section headings |
| `--pos-text-3xl` | 1.875rem (30px) | Page titles |
| `--pos-text-4xl` | 2.25rem (36px) | Large displays |

---

## Spacing Scale

| Token | Size | Pixels |
|-------|------|--------|
| `--pos-space-1` | 0.25rem | 4px |
| `--pos-space-2` | 0.5rem | 8px |
| `--pos-space-3` | 0.75rem | 12px |
| `--pos-space-4` | 1rem | 16px |
| `--pos-space-5` | 1.25rem | 20px |
| `--pos-space-6` | 1.5rem | 24px |
| `--pos-space-8` | 2rem | 32px |
| `--pos-space-10` | 2.5rem | 40px |
| `--pos-space-12` | 3rem | 48px |

---

## Icons (Material Symbols Rounded)

Bundled locally in `app/static/vendor/google/`.

### Usage

```html
<!-- Standard icon -->
<span class="material-symbols-rounded" aria-hidden="true">shopping_cart</span>

<!-- Filled variant -->
<span class="material-symbols-rounded filled" aria-hidden="true">favorite</span>
```

### Size Variants

| Class | Size |
|-------|------|
| `.pos-icon-sm` | 20px |
| (default) | 24px |
| `.pos-icon-lg` | 32px |
| `.pos-icon-xl` | 48px |
