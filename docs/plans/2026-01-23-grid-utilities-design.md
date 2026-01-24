# Grid Utilities Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add CSS Grid utility classes to supplement Materialize's column grid for auto-fit card grids and fixed column layouts.

**Architecture:** New grid utilities follow the same atomic/composable pattern as the flexbox utilities. Base `.grid` class required, then compose with column definitions and existing gap utilities. Responsive variants for fixed columns only (auto-fit is inherently responsive).

**Tech Stack:** CSS Grid, CSS custom properties, Materialize CSS breakpoints

---

## Task 1: Add Base Grid Display and Fixed Column Classes

**Files:**
- Modify: `librepos/app/static/css/utilities.css:183` (insert before Layout Utilities section)

**Step 1: Add grid display and fixed column utilities**

Insert after line 182 (after the responsive flex direction media queries), before the Layout Utilities section:

```css
/* Grid Utilities
   ========================================================================== */

/* Display */
.grid { display: grid; }
.inline-grid { display: inline-grid; }

/* Fixed Column Counts */
.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
.grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.grid-cols-5 { grid-template-columns: repeat(5, minmax(0, 1fr)); }
.grid-cols-6 { grid-template-columns: repeat(6, minmax(0, 1fr)); }
```

**Step 2: Verify CSS is valid**

Run: `npx clean-css-cli librepos/app/static/css/utilities.css -o /dev/null && echo "CSS valid"`
Expected: "CSS valid"

**Step 3: Commit**

```bash
git add librepos/app/static/css/utilities.css
git commit -m "feat(css): add base grid display and column utilities"
```

---

## Task 2: Add Auto-Fit Card Grid Utilities

**Files:**
- Modify: `librepos/app/static/css/utilities.css`

**Step 1: Add auto-fit card utilities after fixed column classes**

```css
/* Auto-Fit Card Grids */
.grid-cards-sm { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }
.grid-cards-md { grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); }
.grid-cards-lg { grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }
```

**Step 2: Verify CSS is valid**

Run: `npx clean-css-cli librepos/app/static/css/utilities.css -o /dev/null && echo "CSS valid"`
Expected: "CSS valid"

**Step 3: Commit**

```bash
git add librepos/app/static/css/utilities.css
git commit -m "feat(css): add auto-fit card grid utilities"
```

---

## Task 3: Add Grid Alignment Utilities

**Files:**
- Modify: `librepos/app/static/css/utilities.css`

**Step 1: Add place-items and place-content utilities after auto-fit cards**

```css
/* Place Items (align content inside each cell) */
.place-items-start { place-items: start; }
.place-items-center { place-items: center; }
.place-items-end { place-items: end; }
.place-items-stretch { place-items: stretch; }

/* Place Content (position the grid within container) */
.place-content-start { place-content: start; }
.place-content-center { place-content: center; }
.place-content-end { place-content: end; }
.place-content-between { place-content: space-between; }
.place-content-around { place-content: space-around; }
.place-content-evenly { place-content: space-evenly; }
```

**Step 2: Verify CSS is valid**

Run: `npx clean-css-cli librepos/app/static/css/utilities.css -o /dev/null && echo "CSS valid"`
Expected: "CSS valid"

**Step 3: Commit**

```bash
git add librepos/app/static/css/utilities.css
git commit -m "feat(css): add grid alignment utilities"
```

---

## Task 4: Add Responsive Grid Column Variants

**Files:**
- Modify: `librepos/app/static/css/utilities.css`

**Step 1: Add responsive column variants after alignment utilities**

```css
/* Responsive Grid Columns (Materialize breakpoints)
   ========================================================================== */

/* Medium screens and up (601px+) */
@media (min-width: 601px) {
    .m\:grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
    .m\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .m\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .m\:grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
    .m\:grid-cols-5 { grid-template-columns: repeat(5, minmax(0, 1fr)); }
    .m\:grid-cols-6 { grid-template-columns: repeat(6, minmax(0, 1fr)); }
}

/* Large screens and up (993px+) */
@media (min-width: 993px) {
    .l\:grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
    .l\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .l\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .l\:grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
    .l\:grid-cols-5 { grid-template-columns: repeat(5, minmax(0, 1fr)); }
    .l\:grid-cols-6 { grid-template-columns: repeat(6, minmax(0, 1fr)); }
}

/* Extra large screens and up (1201px+) */
@media (min-width: 1201px) {
    .xl\:grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
    .xl\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .xl\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .xl\:grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
    .xl\:grid-cols-5 { grid-template-columns: repeat(5, minmax(0, 1fr)); }
    .xl\:grid-cols-6 { grid-template-columns: repeat(6, minmax(0, 1fr)); }
}
```

**Step 2: Verify CSS is valid**

Run: `npx clean-css-cli librepos/app/static/css/utilities.css -o /dev/null && echo "CSS valid"`
Expected: "CSS valid"

**Step 3: Commit**

```bash
git add librepos/app/static/css/utilities.css
git commit -m "feat(css): add responsive grid column utilities"
```

---

## Task 5: Minify CSS

**Files:**
- Modify: `librepos/app/static/css/utilities.min.css`

**Step 1: Minify the utilities CSS**

Run: `npx clean-css-cli -o librepos/app/static/css/utilities.min.css librepos/app/static/css/utilities.css`

**Step 2: Commit minified file**

```bash
git add librepos/app/static/css/utilities.min.css
git commit -m "build(css): minify utilities.css"
```

---

## Usage Examples

```html
<!-- Auto-fit menu items -->
<div class="grid grid-cards-md gap-4">
  <div class="card">Item 1</div>
  <div class="card">Item 2</div>
  <div class="card">Item 3</div>
</div>

<!-- Responsive dashboard widgets -->
<div class="grid grid-cols-1 m:grid-cols-2 l:grid-cols-4 gap-4">
  <div class="card">Widget 1</div>
  <div class="card">Widget 2</div>
  <div class="card">Widget 3</div>
  <div class="card">Widget 4</div>
</div>

<!-- Centered content in grid cells -->
<div class="grid grid-cols-3 gap-4 place-items-center">
  <div>Centered</div>
  <div>Centered</div>
  <div>Centered</div>
</div>
```

## Utility Summary

| Category | Classes | Count |
|----------|---------|-------|
| Display | `.grid`, `.inline-grid` | 2 |
| Fixed columns | `.grid-cols-1` through `.grid-cols-6` | 6 |
| Auto-fit cards | `.grid-cards-sm`, `.grid-cards-md`, `.grid-cards-lg` | 3 |
| Place items | `.place-items-*` | 4 |
| Place content | `.place-content-*` | 6 |
| Responsive columns | `.m:grid-cols-*`, `.l:grid-cols-*`, `.xl:grid-cols-*` | 18 |
| **Total** | | **39 classes** |
