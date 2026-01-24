# Font Size Utility Classes Design

**Date:** 2026-01-24
**Status:** Approved

## Overview

Add font size utility classes to `utilities.css` that reference existing typography tokens from `variables.css`. Includes responsive variants for key sizes.

## Base Classes (8 classes)

```css
.text-xs   { font-size: var(--pos-text-xs); }    /* 12px */
.text-sm   { font-size: var(--pos-text-sm); }    /* 14px */
.text-base { font-size: var(--pos-text-base); }  /* 16px */
.text-lg   { font-size: var(--pos-text-lg); }    /* 18px */
.text-xl   { font-size: var(--pos-text-xl); }    /* 20px */
.text-2xl  { font-size: var(--pos-text-2xl); }   /* 24px */
.text-3xl  { font-size: var(--pos-text-3xl); }   /* 30px */
.text-4xl  { font-size: var(--pos-text-4xl); }   /* 36px */
```

## Responsive Variants (12 classes)

Only key sizes (`text-base`, `text-xl`, `text-2xl`, `text-3xl`) get responsive variants, using existing `m:`, `l:`, `xl:` prefix pattern.

### Medium screens (601px+)
- `.m:text-base`, `.m:text-xl`, `.m:text-2xl`, `.m:text-3xl`

### Large screens (993px+)
- `.l:text-base`, `.l:text-xl`, `.l:text-2xl`, `.l:text-3xl`

### Extra large screens (1201px+)
- `.xl:text-base`, `.xl:text-xl`, `.xl:text-2xl`, `.xl:text-3xl`

## Usage Example

```html
<h1 class="text-xl m:text-2xl l:text-3xl">Menu Categories</h1>
```

Renders at 20px on mobile, 24px on tablets, 30px on desktop.

## Implementation

- **File:** `librepos/app/static/css/utilities.css`
- **Location:** After Grid Utilities section (around line 249)
- **Total classes:** 20 (8 base + 12 responsive)
- **Post-step:** Minify with `npx clean-css-cli`
