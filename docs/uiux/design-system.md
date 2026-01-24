# Design System

> Colors, typography, spacing, and icons

---

## Color Palette (Elegant Restaurant)

All colors defined in `app/static/css/variables.css`. Both themes use warm tones optimized for restaurant environments.

### Theme Overview

| Theme | Background | Text | Primary Accent |
|-------|------------|------|----------------|
| Light | Warm cream `#FAF7F2` | Espresso `#2D2622` | Dark amber `#8B5E00` |
| Dark | Warm charcoal `#1A1614` | Warm white `#F5F0EB` | Amber `#FFB74D` |

### Core Colors (Material Design 3 Tokens)

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `--md-sys-color-background` | `#FAF7F2` | `#1A1614` | Page background |
| `--md-sys-color-surface` | `#F5F0EA` | `#252220` | Cards, panels |
| `--md-sys-color-surface-variant` | `#EDE8E1` | `#302C28` | Elevated surfaces |
| `--md-sys-color-primary` | `#8B5E00` | `#FFB74D` | Key actions, links |
| `--md-sys-color-secondary` | `#5C534A` | `#C9C0B5` | Secondary actions |
| `--md-sys-color-tertiary` | `#4A6355` | `#A8C5B8` | Accent variety (sage) |

### Text Colors

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `--md-sys-color-on-background` | `#2D2622` | `#F5F0EB` | Primary text |
| `--md-sys-color-on-surface-variant` | `#5C534A` | `#A8A099` | Secondary text |
| `--md-sys-color-outline` | `#8A8279` | `#6D665D` | Borders, dividers |

### Semantic Colors (WCAG 2.1 AA)

| Token | Light | Dark | Purpose |
|-------|-------|------|---------|
| `--sys-color-success` | `#2E7D32` | `#81C784` | Order complete, payments |
| `--sys-color-warning` | `#E65100` | `#FFB74D` | Low stock, attention |
| `--sys-color-error` | `#C62828` | `#EF9A9A` | Errors, destructive |
| `--sys-color-info` | `#00796B` | `#4FC3F7` | Tips, informational |

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
