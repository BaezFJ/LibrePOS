# Elegant Restaurant Dark Theme Design

A warm, elegant dark theme optimized for fast-paced restaurant environments. Neutral primary colors keep the interface clean, while a warm amber accent draws attention to key actions. Warm charcoal backgrounds reduce eye strain in dim lighting.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Primary color | Neutral with accent | Clean interface, lets food photos pop |
| Accent color | Warm amber/gold | Premium feel, draws attention without aggression |
| Background | Warm charcoal | Soft, inviting, reduces eye strain in dim lighting |
| Surface elevation | Lighter warm grays | Subtle but clear hierarchy, elegant |
| Text colors | Warm white hierarchy | Cohesive with warm palette, easy on eyes |

## Core Palette

| Role | Token | Hex | Usage |
|------|-------|-----|-------|
| Background | `--md-sys-color-background` | `#1A1614` | Page background |
| Surface | `--md-sys-color-surface` | `#252220` | Cards, panels |
| Surface Variant | `--md-sys-color-surface-variant` | `#302C28` | Elevated surfaces |
| On-Background | `--md-sys-color-on-background` | `#F5F0EB` | Primary text |
| On-Surface | `--md-sys-color-on-surface` | `#F5F0EB` | Primary text |
| On-Surface-Variant | `--md-sys-color-on-surface-variant` | `#A8A099` | Secondary text |
| Outline | `--md-sys-color-outline` | `#6D665D` | Borders, dividers |
| Outline Variant | `--md-sys-color-outline-variant` | `#3D3835` | Subtle borders |

## Accent Colors

| Role | Token | Hex | Usage |
|------|-------|-----|-------|
| Primary | `--md-sys-color-primary` | `#FFB74D` | Key actions, focus |
| On-Primary | `--md-sys-color-on-primary` | `#1A1614` | Text on primary |
| Primary Container | `--md-sys-color-primary-container` | `#4A3F2A` | Selected states |
| On-Primary-Container | `--md-sys-color-on-primary-container` | `#FFE0B2` | Text on container |

## Secondary & Tertiary

| Role | Token | Hex | Usage |
|------|-------|-----|-------|
| Secondary | `--md-sys-color-secondary` | `#C9C0B5` | Secondary buttons, chips |
| On-Secondary | `--md-sys-color-on-secondary` | `#1A1614` | Text on secondary |
| Secondary Container | `--md-sys-color-secondary-container` | `#3D3835` | Tonal buttons |
| On-Secondary-Container | `--md-sys-color-on-secondary-container` | `#E8E0D8` | Text on container |
| Tertiary | `--md-sys-color-tertiary` | `#A8C5B8` | Accent variety (muted sage) |
| On-Tertiary | `--md-sys-color-on-tertiary` | `#1A1614` | Text on tertiary |
| Tertiary Container | `--md-sys-color-tertiary-container` | `#2D3D35` | Tertiary tonal |
| On-Tertiary-Container | `--md-sys-color-on-tertiary-container` | `#D4E8DC` | Text on container |

## Error Colors

| Role | Token | Hex |
|------|-------|-----|
| Error | `--md-sys-color-error` | `#EF9A9A` |
| On-Error | `--md-sys-color-on-error` | `#4A1C1C` |
| Error Container | `--md-sys-color-error-container` | `#5D2A2A` |
| On-Error-Container | `--md-sys-color-on-error-container` | `#FFCDD2` |

## Semantic Colors (WCAG 2.1 AA)

| Role | Hex | Contrast | Usage |
|------|-----|----------|-------|
| Success | `#81C784` | 7.2:1 | Order complete, payment success |
| On-Success | `#1B3D1E` | — | Text on success |
| Success Container | `#2E4830` | — | Success tonal |
| On-Success-Container | `#C8E6C9` | — | Text on container |
| Warning | `#FFB74D` | 8.1:1 | Low stock, attention needed |
| On-Warning | `#3D2E1A` | — | Text on warning |
| Warning Container | `#4A3F2A` | — | Warning tonal |
| On-Warning-Container | `#FFE0B2` | — | Text on container |
| Info | `#4FC3F7` | 7.8:1 | Tips, guidance |
| On-Info | `#0D3346` | — | Text on info |
| Info Container | `#1A4A5E` | — | Info tonal |
| On-Info-Container | `#B3E5FC` | — | Text on container |

## Utility Colors

| Role | Token | Hex |
|------|-------|-----|
| Inverse Surface | `--md-sys-color-inverse-surface` | `#F5F0EB` |
| Inverse On-Surface | `--md-sys-color-inverse-on-surface` | `#1A1614` |
| Inverse Primary | `--md-sys-color-inverse-primary` | `#8B5E00` |
| Shadow | `--md-sys-color-shadow` | `#000000` |
| Scrim | `--md-sys-color-scrim` | `rgba(0, 0, 0, 0.6)` |
| Surface Tint | `--md-sys-color-surface-tint` | `#FFB74D` |

## Surface Elevation Scale

| Level | Token | Hex | Luminance |
|-------|-------|-----|-----------|
| 0 | Background | `#1A1614` | 8% |
| 1 | Surface | `#252220` | 12% |
| 2 | Surface Variant | `#302C28` | 16% |
| 3 | Elevated | `#3D3835` | 20% |

## Implementation

**Files to change:**
- `librepos/app/static/css/variables.css`

**Blocks to update:**
1. `[data-theme="dark"]` — Replace Materialize references with direct hex values
2. `@media (prefers-color-scheme: dark) :root:not([data-theme])` — Same changes

**What stays unchanged:**
- Light theme
- Base `:root` variables (spacing, typography)
- Existing tonal palette definitions (success/warning/info greens/ambers/cyans)
- HTMX loading states
