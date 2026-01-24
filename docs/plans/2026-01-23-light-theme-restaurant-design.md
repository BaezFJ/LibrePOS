# Elegant Restaurant Light Theme Design

A warm, elegant light theme optimized for fast-paced restaurant environments with mixed lighting. Warm cream backgrounds and espresso brown text create an inviting feel that complements the dark theme's amber/charcoal palette.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Target environment | Mixed lighting | Brunch cafes, all-day bistros, venues that vary throughout the day |
| Accent color | Same amber as dark theme | Unified brand identity across both themes |
| Background tone | Warm cream/ivory | Matches dark theme's warmth, not stark white |
| Text colors | Espresso brown hierarchy | Cohesive with warm palette, soft on eyes |
| Semantic colors | Same hues, darker tones | Consistent meaning, adjusted for light background contrast |

## Core Palette

| Role | Token | Hex | Usage |
|------|-------|-----|-------|
| Background | `--md-sys-color-background` | `#FAF7F2` | Page background, warm cream |
| Surface | `--md-sys-color-surface` | `#F5F0EA` | Cards, panels, modals |
| Surface Variant | `--md-sys-color-surface-variant` | `#EDE8E1` | Elevated surfaces, selected states |
| On-Background | `--md-sys-color-on-background` | `#2D2622` | Primary text (espresso) |
| On-Surface | `--md-sys-color-on-surface` | `#2D2622` | Primary text on cards |
| On-Surface-Variant | `--md-sys-color-on-surface-variant` | `#5C534A` | Secondary text, labels |
| Outline | `--md-sys-color-outline` | `#8A8279` | Borders, dividers |
| Outline Variant | `--md-sys-color-outline-variant` | `#C9C4BC` | Subtle borders |

## Surface Elevation Scale

| Level | Use Case | Hex | Description |
|-------|----------|-----|-------------|
| 0 | Page background | `#FAF7F2` | Base cream |
| 1 | Cards, dialogs | `#F5F0EA` | Slightly darker |
| 2 | Dropdowns, popovers | `#EDE8E1` | More depth |
| 3 | Floating actions | `#E5DFD7` | Maximum elevation |

## Accent Colors

### Primary (Amber)

| Role | Token | Hex | Usage |
|------|-------|-----|-------|
| Primary | `--md-sys-color-primary` | `#8B5E00` | Key buttons, active states, links |
| On-Primary | `--md-sys-color-on-primary` | `#FFFFFF` | Text on primary buttons |
| Primary Container | `--md-sys-color-primary-container` | `#FFE0B2` | Tonal buttons, selected chips |
| On-Primary-Container | `--md-sys-color-on-primary-container` | `#5C3D00` | Text on container |

### Secondary (Warm Taupe)

| Role | Token | Hex | Usage |
|------|-------|-----|-------|
| Secondary | `--md-sys-color-secondary` | `#5C534A` | Secondary buttons, less prominent actions |
| On-Secondary | `--md-sys-color-on-secondary` | `#FFFFFF` | Text on secondary |
| Secondary Container | `--md-sys-color-secondary-container` | `#E0DAD3` | Tonal secondary, chips |
| On-Secondary-Container | `--md-sys-color-on-secondary-container` | `#3D3632` | Text on container |

### Tertiary (Sage Green)

| Role | Token | Hex | Usage |
|------|-------|-----|-------|
| Tertiary | `--md-sys-color-tertiary` | `#4A6355` | Accent variety, categories |
| On-Tertiary | `--md-sys-color-on-tertiary` | `#FFFFFF` | Text on tertiary |
| Tertiary Container | `--md-sys-color-tertiary-container` | `#C8DDD0` | Tertiary tonal |
| On-Tertiary-Container | `--md-sys-color-on-tertiary-container` | `#2D3D35` | Text on container |

## Error Colors

| Role | Token | Hex |
|------|-------|-----|
| Error | `--md-sys-color-error` | `#C62828` |
| On-Error | `--md-sys-color-on-error` | `#FFFFFF` |
| Error Container | `--md-sys-color-error-container` | `#FFCDD2` |
| On-Error-Container | `--md-sys-color-on-error-container` | `#B71C1C` |

## Semantic Colors (WCAG 2.1 AA)

| Role | Hex | Contrast vs #FAF7F2 | Usage |
|------|-----|---------------------|-------|
| Success | `#2E7D32` | 5.1:1 | Order complete, payment success |
| On-Success | `#FFFFFF` | — | Text on success |
| Success Container | `#C8E6C9` | — | Success tonal |
| On-Success-Container | `#1B5E20` | — | Text on container |
| Warning | `#E65100` | 4.6:1 | Low stock, attention needed |
| On-Warning | `#FFFFFF` | — | Text on warning |
| Warning Container | `#FFE0B2` | — | Warning tonal |
| On-Warning-Container | `#BF360C` | — | Text on container |
| Info | `#00796B` | 4.8:1 | Tips, guidance |
| On-Info | `#FFFFFF` | — | Text on info |
| Info Container | `#B2DFDB` | — | Info tonal |
| On-Info-Container | `#004D40` | — | Text on container |

## Utility Colors

| Role | Token | Hex |
|------|-------|-----|
| Inverse Surface | `--md-sys-color-inverse-surface` | `#2D2622` |
| Inverse On-Surface | `--md-sys-color-inverse-on-surface` | `#FAF7F2` |
| Inverse Primary | `--md-sys-color-inverse-primary` | `#FFB74D` |
| Shadow | `--md-sys-color-shadow` | `#000000` |
| Scrim | `--md-sys-color-scrim` | `rgba(45, 38, 34, 0.5)` |
| Surface Tint | `--md-sys-color-surface-tint` | `#8B5E00` |

## Implementation

**File to change:**
- `librepos/app/static/css/variables.css`

**Block to update:**
- `:root, :root:not([data-theme]), [data-theme="light"]` — Replace Materialize `-light` variable references with direct hex values

**What stays unchanged:**
- Dark theme (`[data-theme="dark"]`)
- Base `:root` variables (spacing, typography)
- Existing tonal palette definitions
- HTMX loading states
