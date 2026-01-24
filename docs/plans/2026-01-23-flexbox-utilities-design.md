# Flexbox Utilities Redesign Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace opinionated flexbox utilities with atomic, composable classes using Tailwind-style naming.

**Architecture:** New utilities are fully composable (`.flex` required as base, then add direction/alignment). Gap utilities use existing `--pos-space-*` tokens. Responsive variants for direction only, matching Materialize breakpoints.

**Tech Stack:** CSS custom properties, CSS Flexbox, Materialize CSS breakpoints

---

## Task 1: Add Base Flex Display Classes

**Files:**
- Modify: `librepos/app/static/css/utilities.css:57-92`

**Step 1: Add new display utilities after the Flexbox section header**

Replace lines 57-92 (the entire Flexbox Utilities section) with:

```css
/* Flexbox Utilities
   ========================================================================== */

/* Display */
.flex { display: flex; }
.inline-flex { display: inline-flex; }

/* Direction */
.flex-row { flex-direction: row; }
.flex-row-rev { flex-direction: row-reverse; }
.flex-col { flex-direction: column; }
.flex-col-rev { flex-direction: column-reverse; }

/* Wrap */
.flex-wrap { flex-wrap: wrap; }
.flex-nowrap { flex-wrap: nowrap; }
.flex-wrap-rev { flex-wrap: wrap-reverse; }
```

**Step 2: Verify CSS is valid**

Run: `npx clean-css-cli librepos/app/static/css/utilities.css -o /dev/null && echo "CSS valid"`
Expected: "CSS valid"

**Step 3: Commit**

```bash
git add librepos/app/static/css/utilities.css
git commit -m "feat(css): add base flex display utilities"
```

---

## Task 2: Add Alignment Utilities

**Files:**
- Modify: `librepos/app/static/css/utilities.css`

**Step 1: Add alignment classes after wrap utilities**

```css
/* Justify Content (main axis) */
.justify-start { justify-content: flex-start; }
.justify-end { justify-content: flex-end; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.justify-around { justify-content: space-around; }
.justify-evenly { justify-content: space-evenly; }

/* Align Items (cross axis) */
.items-start { align-items: flex-start; }
.items-end { align-items: flex-end; }
.items-center { align-items: center; }
.items-baseline { align-items: baseline; }
.items-stretch { align-items: stretch; }

/* Align Self (individual item override) */
.self-auto { align-self: auto; }
.self-start { align-self: flex-start; }
.self-end { align-self: flex-end; }
.self-center { align-self: center; }
.self-stretch { align-self: stretch; }
```

**Step 2: Verify CSS is valid**

Run: `npx clean-css-cli librepos/app/static/css/utilities.css -o /dev/null && echo "CSS valid"`
Expected: "CSS valid"

**Step 3: Commit**

```bash
git add librepos/app/static/css/utilities.css
git commit -m "feat(css): add flexbox alignment utilities"
```

---

## Task 3: Add Gap Utilities

**Files:**
- Modify: `librepos/app/static/css/utilities.css`

**Step 1: Add gap classes using existing spacing tokens**

```css
/* Gap (both axes) */
.gap-0 { gap: 0; }
.gap-1 { gap: var(--pos-space-1); }
.gap-2 { gap: var(--pos-space-2); }
.gap-3 { gap: var(--pos-space-3); }
.gap-4 { gap: var(--pos-space-4); }
.gap-5 { gap: var(--pos-space-5); }
.gap-6 { gap: var(--pos-space-6); }
.gap-8 { gap: var(--pos-space-8); }
.gap-10 { gap: var(--pos-space-10); }
.gap-12 { gap: var(--pos-space-12); }

/* Column Gap (horizontal spacing) */
.gap-x-0 { column-gap: 0; }
.gap-x-1 { column-gap: var(--pos-space-1); }
.gap-x-2 { column-gap: var(--pos-space-2); }
.gap-x-3 { column-gap: var(--pos-space-3); }
.gap-x-4 { column-gap: var(--pos-space-4); }
.gap-x-5 { column-gap: var(--pos-space-5); }
.gap-x-6 { column-gap: var(--pos-space-6); }
.gap-x-8 { column-gap: var(--pos-space-8); }
.gap-x-10 { column-gap: var(--pos-space-10); }
.gap-x-12 { column-gap: var(--pos-space-12); }

/* Row Gap (vertical spacing) */
.gap-y-0 { row-gap: 0; }
.gap-y-1 { row-gap: var(--pos-space-1); }
.gap-y-2 { row-gap: var(--pos-space-2); }
.gap-y-3 { row-gap: var(--pos-space-3); }
.gap-y-4 { row-gap: var(--pos-space-4); }
.gap-y-5 { row-gap: var(--pos-space-5); }
.gap-y-6 { row-gap: var(--pos-space-6); }
.gap-y-8 { row-gap: var(--pos-space-8); }
.gap-y-10 { row-gap: var(--pos-space-10); }
.gap-y-12 { row-gap: var(--pos-space-12); }
```

**Step 2: Verify CSS is valid**

Run: `npx clean-css-cli librepos/app/static/css/utilities.css -o /dev/null && echo "CSS valid"`
Expected: "CSS valid"

**Step 3: Commit**

```bash
git add librepos/app/static/css/utilities.css
git commit -m "feat(css): add flexbox gap utilities"
```

---

## Task 4: Add Flex Grow/Shrink/Basis Utilities

**Files:**
- Modify: `librepos/app/static/css/utilities.css`

**Step 1: Add flex item control classes**

```css
/* Flex Shorthand */
.flex-1 { flex: 1 1 0%; }
.flex-auto { flex: 1 1 auto; }
.flex-initial { flex: 0 1 auto; }
.flex-none { flex: none; }

/* Flex Grow */
.grow-0 { flex-grow: 0; }
.grow { flex-grow: 1; }

/* Flex Shrink */
.shrink-0 { flex-shrink: 0; }
.shrink { flex-shrink: 1; }

/* Flex Basis */
.basis-0 { flex-basis: 0; }
.basis-auto { flex-basis: auto; }
.basis-full { flex-basis: 100%; }
.basis-1\/2 { flex-basis: 50%; }
.basis-1\/3 { flex-basis: 33.333%; }
.basis-2\/3 { flex-basis: 66.667%; }
.basis-1\/4 { flex-basis: 25%; }
.basis-3\/4 { flex-basis: 75%; }
```

**Step 2: Verify CSS is valid**

Run: `npx clean-css-cli librepos/app/static/css/utilities.css -o /dev/null && echo "CSS valid"`
Expected: "CSS valid"

**Step 3: Commit**

```bash
git add librepos/app/static/css/utilities.css
git commit -m "feat(css): add flex grow/shrink/basis utilities"
```

---

## Task 5: Add Responsive Direction Classes

**Files:**
- Modify: `librepos/app/static/css/utilities.css`

**Step 1: Add responsive variants at end of flexbox section**

```css
/* Responsive Direction (Materialize breakpoints)
   ========================================================================== */

/* Medium screens and up (601px+) */
@media (min-width: 601px) {
    .m\:flex-row { flex-direction: row; }
    .m\:flex-row-rev { flex-direction: row-reverse; }
    .m\:flex-col { flex-direction: column; }
    .m\:flex-col-rev { flex-direction: column-reverse; }
}

/* Large screens and up (993px+) */
@media (min-width: 993px) {
    .l\:flex-row { flex-direction: row; }
    .l\:flex-row-rev { flex-direction: row-reverse; }
    .l\:flex-col { flex-direction: column; }
    .l\:flex-col-rev { flex-direction: column-reverse; }
}

/* Extra large screens and up (1201px+) */
@media (min-width: 1201px) {
    .xl\:flex-row { flex-direction: row; }
    .xl\:flex-row-rev { flex-direction: row-reverse; }
    .xl\:flex-col { flex-direction: column; }
    .xl\:flex-col-rev { flex-direction: column-reverse; }
}
```

**Step 2: Verify CSS is valid**

Run: `npx clean-css-cli librepos/app/static/css/utilities.css -o /dev/null && echo "CSS valid"`
Expected: "CSS valid"

**Step 3: Commit**

```bash
git add librepos/app/static/css/utilities.css
git commit -m "feat(css): add responsive flex direction utilities"
```

---

## Task 6: Update center-content Layout Utility

**Files:**
- Modify: `librepos/app/static/css/utilities.css`

**Step 1: Update center-content to use navbar variable**

Find the `.center-content` rule and update it:

```css
.center-content {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: calc(100vh - var(--navbar-height, 64px));
}
```

**Step 2: Verify CSS is valid**

Run: `npx clean-css-cli librepos/app/static/css/utilities.css -o /dev/null && echo "CSS valid"`
Expected: "CSS valid"

**Step 3: Commit**

```bash
git add librepos/app/static/css/utilities.css
git commit -m "fix(css): use navbar variable in center-content"
```

---

## Task 7: Migrate Template Usages

**Files:**
- Modify: `librepos/app/templates/macros/modals.html:82,119`
- Modify: `librepos/app/blueprints/menu/templates/menu/categories.html:13,19`

**Step 1: Update modals.html line 82**

Change: `class="modal-header flex-row space-between"`
To: `class="modal-header flex flex-row items-center justify-between"`

**Step 2: Update modals.html line 119**

Change: `class="modal-header flex-row space-between"`
To: `class="modal-header flex flex-row items-center justify-between"`

**Step 3: Update categories.html line 13**

Change: `class="flex-row space-between"`
To: `class="flex flex-row items-center justify-between"`

**Step 4: Update categories.html line 19**

Change: `class="flex-row space-between"`
To: `class="flex flex-row items-center justify-between"`

**Step 5: Commit**

```bash
git add librepos/app/templates/macros/modals.html librepos/app/blueprints/menu/templates/menu/categories.html
git commit -m "refactor: migrate templates to new flexbox utilities"
```

---

## Task 8: Minify CSS and Final Commit

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

## Migration Reference

| Old Class | New Classes |
|-----------|-------------|
| `.flex-row` | `.flex .flex-row .items-center` |
| `.flex-col` | `.flex .flex-col .items-center` |
| `.flex-wrap` (old) | `.flex .flex-wrap .items-center` |
| `.space-between` | `.justify-between` |
| `.space-around` | `.justify-around` |
| `.flex-align-center` | `.items-center` |
| `.justify-flex-end` | `.justify-end` |

## Usage Examples

```html
<!-- Center everything -->
<div class="flex items-center justify-center">...</div>

<!-- Space between with vertical center -->
<div class="flex justify-between items-center">...</div>

<!-- Stack on mobile, row on tablet+ -->
<div class="flex flex-col m:flex-row gap-4">...</div>

<!-- Fill remaining space -->
<div class="flex">
  <div class="shrink-0">Fixed</div>
  <div class="flex-1">Fills remaining</div>
</div>
```