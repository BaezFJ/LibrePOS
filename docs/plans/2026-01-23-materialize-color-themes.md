# MaterializeCSS Color Themes Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rewrite LibrePOS color themes using only MaterializeCSS color variables with WCAG 2.1 AA compliance.

**Architecture:** Remove Catppuccin palette and `--pos-*` color layer. Use Materialize's built-in `--md-sys-color-*-light/dark` tokens directly. Add custom tonal scales for success/warning/info semantic colors.

**Tech Stack:** CSS custom properties, MaterializeCSS 2.2.2, Material Design 3 color system

**Design Document:** `docs/plans/2026-01-23-materialize-color-themes-design.md`

---

## Task 1: Rewrite variables.css - Base Variables Section

**Files:**
- Modify: `librepos/app/static/css/variables.css:1-53`

**Step 1: Replace file header and base variables**

Replace lines 1-53 with:

```css
/*
 * LibrePOS Design System Variables
 * ================================
 * CSS custom properties following Material Design 3 color system.
 * Uses MaterializeCSS 2.2.2 built-in tokens with custom semantic palettes.
 *
 * Usage:
 *   - Theme toggle: <html data-theme="dark"> or <html data-theme="light">
 *   - Auto-detect: Remove data-theme attribute to follow system preference
 *
 * References:
 *   - Full design system: docs/uiux.md
 *   - MaterializeCSS: https://materializeweb.com
 */

/* =============================================================================
   BASE VARIABLES (Theme-Independent)
   ============================================================================= */
:root {
    /* ── Typography ── */
    --pos-font-family: system-ui, -apple-system, BlinkMacSystemFont,
                       'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    --pos-font-mono: ui-monospace, 'SF Mono', Monaco, 'Cascadia Code', monospace;

    /* Font Sizes - Touch-optimized minimums */
    --pos-text-xs: 0.75rem;    /* 12px - minimum for labels */
    --pos-text-sm: 0.875rem;   /* 14px */
    --pos-text-base: 1rem;     /* 16px - body text minimum */
    --pos-text-lg: 1.125rem;   /* 18px */
    --pos-text-xl: 1.25rem;    /* 20px */
    --pos-text-2xl: 1.5rem;    /* 24px */
    --pos-text-3xl: 1.875rem;  /* 30px */
    --pos-text-4xl: 2.25rem;   /* 36px - large displays */

    /* ── Spacing Scale ── */
    --pos-space-1: 0.25rem;   /* 4px */
    --pos-space-2: 0.5rem;    /* 8px */
    --pos-space-3: 0.75rem;   /* 12px */
    --pos-space-4: 1rem;      /* 16px */
    --pos-space-5: 1.25rem;   /* 20px */
    --pos-space-6: 1.5rem;    /* 24px */
    --pos-space-8: 2rem;      /* 32px */
    --pos-space-10: 2.5rem;   /* 40px */
    --pos-space-12: 3rem;     /* 48px */

    /* ── Layout ── */
    --navbar-height: 64px;
    --navbar-height-mobile: 56px;
```

**Step 2: Verify syntax**

Run: `cat librepos/app/static/css/variables.css | head -60`
Expected: New header and base variables without Catppuccin references

---

## Task 2: Add Custom Tonal Palettes

**Files:**
- Modify: `librepos/app/static/css/variables.css` (append to :root block from Task 1)

**Step 1: Add success, warning, info tonal scales**

Add after the layout variables (before the closing `}` of `:root`):

```css

    /* ══════════════════════════════════════════════════════════════════════════
       CUSTOM TONAL PALETTES (Success, Warning, Info)
       Following Material Design 3 tonal scale pattern (0-100)
       ══════════════════════════════════════════════════════════════════════════ */

    /* ── Success (Green) - Source: #1B7D3E ── */
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

    /* ── Warning (Amber) - Source: #8B5000 ── */
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

    /* ── Info (Cyan) - Source: #006879 ── */
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
}
```

**Step 2: Verify tonal palettes added**

Run: `grep -c "md-ref-palette-success\|md-ref-palette-warning\|md-ref-palette-info" librepos/app/static/css/variables.css`
Expected: 39 (13 tones × 3 palettes)

---

## Task 3: Add Light Theme Section

**Files:**
- Modify: `librepos/app/static/css/variables.css` (add after :root block)

**Step 1: Add light theme with Material tokens and semantic colors**

Add after the `:root` block closing brace:

```css


/* =============================================================================
   LIGHT THEME (Default)
   ============================================================================= */
:root,
:root:not([data-theme]),
[data-theme="light"] {
    color-scheme: light;

    /* ══════════════════════════════════════════════════════════════════════════
       Material Design System Colors - Light
       Override Materialize defaults to ensure consistent theming
       ══════════════════════════════════════════════════════════════════════════ */
    --md-sys-color-primary: var(--md-sys-color-primary-light);
    --md-sys-color-on-primary: var(--md-sys-color-on-primary-light);
    --md-sys-color-primary-container: var(--md-sys-color-primary-container-light);
    --md-sys-color-on-primary-container: var(--md-sys-color-on-primary-container-light);

    --md-sys-color-secondary: var(--md-sys-color-secondary-light);
    --md-sys-color-on-secondary: var(--md-sys-color-on-secondary-light);
    --md-sys-color-secondary-container: var(--md-sys-color-secondary-container-light);
    --md-sys-color-on-secondary-container: var(--md-sys-color-on-secondary-container-light);

    --md-sys-color-tertiary: var(--md-sys-color-tertiary-light);
    --md-sys-color-on-tertiary: var(--md-sys-color-on-tertiary-light);
    --md-sys-color-tertiary-container: var(--md-sys-color-tertiary-container-light);
    --md-sys-color-on-tertiary-container: var(--md-sys-color-on-tertiary-container-light);

    --md-sys-color-error: var(--md-sys-color-error-light);
    --md-sys-color-on-error: var(--md-sys-color-on-error-light);
    --md-sys-color-error-container: var(--md-sys-color-error-container-light);
    --md-sys-color-on-error-container: var(--md-sys-color-on-error-container-light);

    --md-sys-color-background: var(--md-sys-color-background-light);
    --md-sys-color-on-background: var(--md-sys-color-on-background-light);
    --md-sys-color-surface: var(--md-sys-color-surface-light);
    --md-sys-color-on-surface: var(--md-sys-color-on-surface-light);

    --md-sys-color-surface-variant: var(--md-sys-color-surface-variant-light);
    --md-sys-color-on-surface-variant: var(--md-sys-color-on-surface-variant-light);

    --md-sys-color-outline: var(--md-sys-color-outline-light);
    --md-sys-color-outline-variant: var(--md-sys-color-outline-variant-light);

    --md-sys-color-inverse-surface: var(--md-sys-color-inverse-surface-light);
    --md-sys-color-inverse-on-surface: var(--md-sys-color-inverse-on-surface-light);
    --md-sys-color-inverse-primary: var(--md-sys-color-inverse-primary-light);

    --md-sys-color-shadow: var(--md-sys-color-shadow-light);
    --md-sys-color-scrim: var(--md-sys-color-scrim-light);
    --md-sys-color-surface-tint: var(--md-sys-color-surface-tint-light);

    /* ══════════════════════════════════════════════════════════════════════════
       Custom Semantic Colors - Light
       WCAG 2.1 AA compliant (4.5:1 minimum contrast)
       ══════════════════════════════════════════════════════════════════════════ */

    /* ── Success ── */
    --sys-color-success: var(--md-ref-palette-success40);
    --sys-color-on-success: #ffffff;
    --sys-color-success-container: var(--md-ref-palette-success90);
    --sys-color-on-success-container: var(--md-ref-palette-success10);

    /* ── Warning ── */
    --sys-color-warning: var(--md-ref-palette-warning40);
    --sys-color-on-warning: #ffffff;
    --sys-color-warning-container: var(--md-ref-palette-warning90);
    --sys-color-on-warning-container: var(--md-ref-palette-warning10);

    /* ── Info ── */
    --sys-color-info: var(--md-ref-palette-info40);
    --sys-color-on-info: #ffffff;
    --sys-color-info-container: var(--md-ref-palette-info90);
    --sys-color-on-info-container: var(--md-ref-palette-info10);

    /* ── Error (alias for consistency) ── */
    --sys-color-error: var(--md-sys-color-error);
    --sys-color-on-error: var(--md-sys-color-on-error);
    --sys-color-error-container: var(--md-sys-color-error-container);
    --sys-color-on-error-container: var(--md-sys-color-on-error-container);
}
```

**Step 2: Verify light theme added**

Run: `grep -c "sys-color-success\|sys-color-warning\|sys-color-info" librepos/app/static/css/variables.css`
Expected: 12 (4 tokens × 3 semantic colors)

---

## Task 4: Add Dark Theme Section

**Files:**
- Modify: `librepos/app/static/css/variables.css` (add after light theme block)

**Step 1: Add dark theme with Material tokens and semantic colors**

Add after the light theme block closing brace:

```css


/* =============================================================================
   DARK THEME
   ============================================================================= */
[data-theme="dark"] {
    color-scheme: dark;

    /* ══════════════════════════════════════════════════════════════════════════
       Material Design System Colors - Dark
       ══════════════════════════════════════════════════════════════════════════ */
    --md-sys-color-primary: var(--md-sys-color-primary-dark);
    --md-sys-color-on-primary: var(--md-sys-color-on-primary-dark);
    --md-sys-color-primary-container: var(--md-sys-color-primary-container-dark);
    --md-sys-color-on-primary-container: var(--md-sys-color-on-primary-container-dark);

    --md-sys-color-secondary: var(--md-sys-color-secondary-dark);
    --md-sys-color-on-secondary: var(--md-sys-color-on-secondary-dark);
    --md-sys-color-secondary-container: var(--md-sys-color-secondary-container-dark);
    --md-sys-color-on-secondary-container: var(--md-sys-color-on-secondary-container-dark);

    --md-sys-color-tertiary: var(--md-sys-color-tertiary-dark);
    --md-sys-color-on-tertiary: var(--md-sys-color-on-tertiary-dark);
    --md-sys-color-tertiary-container: var(--md-sys-color-tertiary-container-dark);
    --md-sys-color-on-tertiary-container: var(--md-sys-color-on-tertiary-container-dark);

    --md-sys-color-error: var(--md-sys-color-error-dark);
    --md-sys-color-on-error: var(--md-sys-color-on-error-dark);
    --md-sys-color-error-container: var(--md-sys-color-error-container-dark);
    --md-sys-color-on-error-container: var(--md-sys-color-on-error-container-dark);

    --md-sys-color-background: var(--md-sys-color-background-dark);
    --md-sys-color-on-background: var(--md-sys-color-on-background-dark);
    --md-sys-color-surface: var(--md-sys-color-surface-dark);
    --md-sys-color-on-surface: var(--md-sys-color-on-surface-dark);

    --md-sys-color-surface-variant: var(--md-sys-color-surface-variant-dark);
    --md-sys-color-on-surface-variant: var(--md-sys-color-on-surface-variant-dark);

    --md-sys-color-outline: var(--md-sys-color-outline-dark);
    --md-sys-color-outline-variant: var(--md-sys-color-outline-variant-dark);

    --md-sys-color-inverse-surface: var(--md-sys-color-inverse-surface-dark);
    --md-sys-color-inverse-on-surface: var(--md-sys-color-inverse-on-surface-dark);
    --md-sys-color-inverse-primary: var(--md-sys-color-inverse-primary-dark);

    --md-sys-color-shadow: var(--md-sys-color-shadow-dark);
    --md-sys-color-scrim: var(--md-sys-color-scrim-dark);
    --md-sys-color-surface-tint: var(--md-sys-color-surface-tint-dark);

    /* ══════════════════════════════════════════════════════════════════════════
       Custom Semantic Colors - Dark
       WCAG 2.1 AA compliant (4.5:1 minimum contrast)
       ══════════════════════════════════════════════════════════════════════════ */

    /* ── Success ── */
    --sys-color-success: var(--md-ref-palette-success80);
    --sys-color-on-success: var(--md-ref-palette-success20);
    --sys-color-success-container: var(--md-ref-palette-success30);
    --sys-color-on-success-container: var(--md-ref-palette-success90);

    /* ── Warning ── */
    --sys-color-warning: var(--md-ref-palette-warning80);
    --sys-color-on-warning: var(--md-ref-palette-warning20);
    --sys-color-warning-container: var(--md-ref-palette-warning30);
    --sys-color-on-warning-container: var(--md-ref-palette-warning90);

    /* ── Info ── */
    --sys-color-info: var(--md-ref-palette-info80);
    --sys-color-on-info: var(--md-ref-palette-info20);
    --sys-color-info-container: var(--md-ref-palette-info30);
    --sys-color-on-info-container: var(--md-ref-palette-info90);

    /* ── Error (alias for consistency) ── */
    --sys-color-error: var(--md-sys-color-error);
    --sys-color-on-error: var(--md-sys-color-on-error);
    --sys-color-error-container: var(--md-sys-color-error-container);
    --sys-color-on-error-container: var(--md-sys-color-on-error-container);
}
```

**Step 2: Verify dark theme selector exists**

Run: `grep '\[data-theme="dark"\]' librepos/app/static/css/variables.css | head -1`
Expected: `[data-theme="dark"] {`

---

## Task 5: Add System Preference Fallback

**Files:**
- Modify: `librepos/app/static/css/variables.css` (add after dark theme block)

**Step 1: Add prefers-color-scheme media query**

Add after the dark theme block closing brace:

```css


/* =============================================================================
   SYSTEM PREFERENCE FALLBACK
   Applies dark theme when no data-theme attribute and system prefers dark
   ============================================================================= */
@media (prefers-color-scheme: dark) {
    :root:not([data-theme]) {
        color-scheme: dark;

        /* Material Design System Colors - Dark */
        --md-sys-color-primary: var(--md-sys-color-primary-dark);
        --md-sys-color-on-primary: var(--md-sys-color-on-primary-dark);
        --md-sys-color-primary-container: var(--md-sys-color-primary-container-dark);
        --md-sys-color-on-primary-container: var(--md-sys-color-on-primary-container-dark);

        --md-sys-color-secondary: var(--md-sys-color-secondary-dark);
        --md-sys-color-on-secondary: var(--md-sys-color-on-secondary-dark);
        --md-sys-color-secondary-container: var(--md-sys-color-secondary-container-dark);
        --md-sys-color-on-secondary-container: var(--md-sys-color-on-secondary-container-dark);

        --md-sys-color-tertiary: var(--md-sys-color-tertiary-dark);
        --md-sys-color-on-tertiary: var(--md-sys-color-on-tertiary-dark);
        --md-sys-color-tertiary-container: var(--md-sys-color-tertiary-container-dark);
        --md-sys-color-on-tertiary-container: var(--md-sys-color-on-tertiary-container-dark);

        --md-sys-color-error: var(--md-sys-color-error-dark);
        --md-sys-color-on-error: var(--md-sys-color-on-error-dark);
        --md-sys-color-error-container: var(--md-sys-color-error-container-dark);
        --md-sys-color-on-error-container: var(--md-sys-color-on-error-container-dark);

        --md-sys-color-background: var(--md-sys-color-background-dark);
        --md-sys-color-on-background: var(--md-sys-color-on-background-dark);
        --md-sys-color-surface: var(--md-sys-color-surface-dark);
        --md-sys-color-on-surface: var(--md-sys-color-on-surface-dark);

        --md-sys-color-surface-variant: var(--md-sys-color-surface-variant-dark);
        --md-sys-color-on-surface-variant: var(--md-sys-color-on-surface-variant-dark);

        --md-sys-color-outline: var(--md-sys-color-outline-dark);
        --md-sys-color-outline-variant: var(--md-sys-color-outline-variant-dark);

        --md-sys-color-inverse-surface: var(--md-sys-color-inverse-surface-dark);
        --md-sys-color-inverse-on-surface: var(--md-sys-color-inverse-on-surface-dark);
        --md-sys-color-inverse-primary: var(--md-sys-color-inverse-primary-dark);

        --md-sys-color-shadow: var(--md-sys-color-shadow-dark);
        --md-sys-color-scrim: var(--md-sys-color-scrim-dark);
        --md-sys-color-surface-tint: var(--md-sys-color-surface-tint-dark);

        /* Custom Semantic Colors - Dark */
        --sys-color-success: var(--md-ref-palette-success80);
        --sys-color-on-success: var(--md-ref-palette-success20);
        --sys-color-success-container: var(--md-ref-palette-success30);
        --sys-color-on-success-container: var(--md-ref-palette-success90);

        --sys-color-warning: var(--md-ref-palette-warning80);
        --sys-color-on-warning: var(--md-ref-palette-warning20);
        --sys-color-warning-container: var(--md-ref-palette-warning30);
        --sys-color-on-warning-container: var(--md-ref-palette-warning90);

        --sys-color-info: var(--md-ref-palette-info80);
        --sys-color-on-info: var(--md-ref-palette-info20);
        --sys-color-info-container: var(--md-ref-palette-info30);
        --sys-color-on-info-container: var(--md-ref-palette-info90);

        --sys-color-error: var(--md-sys-color-error);
        --sys-color-on-error: var(--md-sys-color-on-error);
        --sys-color-error-container: var(--md-sys-color-error-container);
        --sys-color-on-error-container: var(--md-sys-color-on-error-container);
    }
}
```

**Step 2: Verify media query exists**

Run: `grep "prefers-color-scheme: dark" librepos/app/static/css/variables.css`
Expected: `@media (prefers-color-scheme: dark) {`

---

## Task 6: Add HTMX Loading States

**Files:**
- Modify: `librepos/app/static/css/variables.css` (add at end of file)

**Step 1: Add HTMX loading states**

Add at the end of the file:

```css


/* =============================================================================
   HTMX Loading States
   ============================================================================= */
.htmx-indicator {
    display: none;
}

.htmx-request .htmx-indicator {
    display: block;
}

.htmx-request table,
.htmx-request .collection {
    opacity: 0.5;
    pointer-events: none;
    transition: opacity 0.2s ease;
}
```

**Step 2: Verify HTMX states added**

Run: `grep "htmx-indicator" librepos/app/static/css/variables.css`
Expected: Shows `.htmx-indicator` rules

**Step 3: Verify no Catppuccin references remain**

Run: `grep -c "ctp-\|catppuccin\|Catppuccin" librepos/app/static/css/variables.css`
Expected: 0

**Step 4: Commit variables.css rewrite**

```bash
git add librepos/app/static/css/variables.css
git commit -m "feat(css): rewrite color themes with MaterializeCSS tokens

- Remove Catppuccin color palette dependency
- Use MaterializeCSS built-in --md-sys-color-*-light/dark tokens
- Add custom tonal scales for success/warning/info (WCAG 2.1 AA)
- Maintain data-theme toggle and prefers-color-scheme fallback
- Keep --pos-space-*, --pos-text-*, --pos-font-* unchanged

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 7: Update utilities.css

**Files:**
- Modify: `librepos/app/static/css/utilities.css:183-190`

**Step 1: Update focusable skip link colors**

Change lines 183-190 from:

```css
.pos-sr-only--focusable:focus {
    position: static;
    width: auto;
    height: auto;
    padding: var(--pos-space-2) var(--pos-space-4);
    margin: 0;
    overflow: visible;
    clip: auto;
    white-space: normal;
    background-color: var(--pos-bg-primary);
    color: var(--pos-text-primary);
    z-index: 9999;
}
```

To:

```css
.pos-sr-only--focusable:focus {
    position: static;
    width: auto;
    height: auto;
    padding: var(--pos-space-2) var(--pos-space-4);
    margin: 0;
    overflow: visible;
    clip: auto;
    white-space: normal;
    background-color: var(--md-sys-color-surface);
    color: var(--md-sys-color-on-surface);
    z-index: 9999;
}
```

**Step 2: Verify no --pos- color variables remain in utilities.css**

Run: `grep "pos-bg-\|pos-text-primary\|pos-border" librepos/app/static/css/utilities.css`
Expected: No output (no matches)

**Step 3: Commit utilities.css update**

```bash
git add librepos/app/static/css/utilities.css
git commit -m "fix(css): migrate skip link to Material Design tokens

Replace --pos-bg-primary and --pos-text-primary with
--md-sys-color-surface and --md-sys-color-on-surface.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 8: Update Documentation

**Files:**
- Modify: `docs/uiux.md:35-37`
- Modify: `docs/uiux.md:100`

**Step 1: Update CSS files table**

Change line 35-37 from:

```markdown
| File | Purpose |
|------|---------|
| `variables.css` | Design tokens (Catppuccin colors, spacing, typography) |
```

To:

```markdown
| File | Purpose |
|------|---------|
| `variables.css` | Design tokens (MaterializeCSS colors, spacing, typography) |
```

**Step 2: Update theme system description**

Change line 100 from:

```markdown
Light theme: Catppuccin Latte | Dark theme: Catppuccin Mocha
```

To:

```markdown
Light theme: MaterializeCSS default | Dark theme: MaterializeCSS dark
```

**Step 3: Verify documentation updated**

Run: `grep -i "catppuccin" docs/uiux.md`
Expected: No output (no matches)

**Step 4: Commit documentation update**

```bash
git add docs/uiux.md
git commit -m "docs: update uiux.md for MaterializeCSS color system

Remove Catppuccin references, document MaterializeCSS token usage.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 9: Regenerate Minified CSS

**Files:**
- Regenerate: `librepos/app/static/css/variables.min.css`
- Regenerate: `librepos/app/static/css/utilities.min.css`

**Step 1: Check if minification tooling exists**

Run: `ls package.json 2>/dev/null || ls Makefile 2>/dev/null || echo "No build tooling found"`

**Step 2: If no tooling, manually copy (or skip if build process handles it)**

If minification is manual, the minified files will be regenerated on next build/deploy.

**Step 3: Verify CSS syntax is valid**

Run: `python3 -c "import cssutils; cssutils.parseFile('librepos/app/static/css/variables.css')" 2>/dev/null || echo "cssutils not installed, skip validation"`

---

## Task 10: Visual Verification

**Step 1: Start development server**

Run: `flask run`

**Step 2: Test light theme**

Open browser to http://localhost:5000
Verify: Page loads with light theme colors

**Step 3: Test dark theme toggle**

Open browser console, run: `document.documentElement.setAttribute('data-theme', 'dark')`
Verify: Page switches to dark theme colors

**Step 4: Test system preference**

Open browser console, run: `document.documentElement.removeAttribute('data-theme')`
Verify: Page follows system preference

**Step 5: Test semantic colors**

Navigate to a page with success/warning/info feedback elements
Verify: Colors display correctly and are readable

---

## Task 11: Final Verification and Cleanup

**Step 1: Verify no Catppuccin references in CSS**

Run: `grep -ri "ctp-\|catppuccin" librepos/app/static/css/`
Expected: No matches (or only in .min.css files that need regeneration)

**Step 2: Verify no orphaned --pos- color variables**

Run: `grep -r "pos-primary\|pos-secondary\|pos-accent\|pos-success\|pos-warning\|pos-danger\|pos-info\|pos-bg-\|pos-text-primary\|pos-text-secondary\|pos-text-muted\|pos-border\|pos-shadow" librepos/app/static/css/*.css librepos/app/blueprints/*/static/css/*.css 2>/dev/null | grep -v ".min.css"`
Expected: No matches

**Step 3: Run tests**

Run: `pytest`
Expected: All tests pass

**Step 4: Create summary commit if needed**

If all tasks completed successfully:

```bash
git log --oneline -5
```

Verify: Shows commits for variables.css, utilities.css, and uiux.md
