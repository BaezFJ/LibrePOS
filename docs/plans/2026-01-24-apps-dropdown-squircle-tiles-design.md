# Apps Dropdown Squircle Tiles Design

## Overview

Redesign the apps dropdown to use individual squircle-styled tiles for each application icon, inspired by modern iOS-like card aesthetics with smooth, large corner radii.

## Goals

- Give each app tile a distinct, elevated card appearance
- Use extra-large border radius (24px) for smooth squircle effect
- Maintain subtle container background that doesn't compete with tiles
- Preserve touch-friendly sizing and accessibility standards

## Visual Design

### Tile Specifications

| Property | Value |
|----------|-------|
| Border radius | 24px (`--pos-radius-2xl`) |
| Background (rest) | `--md-sys-color-surface-container` |
| Background (hover) | `--md-sys-color-surface-container-high` |
| Size | ~80x80px |
| Padding | 16px |

### Container Specifications

| Property | Value |
|----------|-------|
| Border radius | 16px (`--pos-radius-xl`) |
| Background | `--md-sys-color-surface-container-low` |
| Padding | 16px |
| Width | 320px |

### Grid Layout

| Property | Value |
|----------|-------|
| Columns | 3 |
| Gap | 12px |

## Interaction States

### Hover
- Background: `surface-container-high`
- Transform: `scale(1.02)`
- Transition: `150ms ease`

### Focus (keyboard)
- Outline: 2px solid `--md-sys-color-primary`
- Outline offset: 2px

### Active/Pressed
- Transform: `scale(0.98)`

## Accessibility

- Touch targets: 80x80px (exceeds 48px minimum)
- Gap between targets: 12px (exceeds 8px minimum)
- Focus indicators: visible outline with offset
- Color contrast: inherits from theme system

## Implementation

### Files to Modify

1. **`librepos/app/static/css/variables.css`**
   - Add `--pos-radius-2xl: 24px`

2. **`librepos/app/static/css/main.css`**
   - Update `.apps-dropdown` container styles
   - Update `.app-tile` with squircle styling
   - Add interaction state rules

3. **Minified files**
   - Regenerate `main.min.css`

### No Changes Required

- HTML templates (existing macro structure works)
- JavaScript (Materialize dropdown behavior unchanged)
- Dropdown component macro (`_dropdown.html`)

## CSS Changes

### New Variable

```css
--pos-radius-2xl: 24px;
```

### Updated `.apps-dropdown`

```css
.dropdown-content.apps-dropdown {
    padding: var(--pos-space-4);
    width: 320px;
    border-radius: var(--pos-radius-xl);
    background: var(--md-sys-color-surface-container-low);
}
```

### Updated `.app-tile`

```css
.app-tile {
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: var(--pos-space-2);
    padding: var(--pos-space-4);
    min-height: 80px;
    min-width: 80px;
    border-radius: var(--pos-radius-2xl);
    background: var(--md-sys-color-surface-container);
    border: none;
    transition: background-color 150ms ease, transform 150ms ease;
}

.app-tile:hover {
    background: var(--md-sys-color-surface-container-high);
    transform: scale(1.02);
}

.app-tile:focus-visible {
    outline: 2px solid var(--md-sys-color-primary);
    outline-offset: 2px;
}

.app-tile:active {
    transform: scale(0.98);
}
```

### Updated `.apps-grid`

```css
.apps-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--pos-space-3);
}
```
