# Touch & Responsive Design

> Touch targets, interactions, and breakpoints

---

## Touch Targets

| Size | Usage |
|------|-------|
| **44x44px** | Minimum (WCAG 2.1 AAA) |
| **48x48px** | Recommended |
| **56px height** | Menu items (frequent taps) |
| **8px gap** | Minimum between targets |

---

## Touch Interactions

```javascript
// Use pointer events for cross-device compatibility
element.addEventListener('pointerdown', () => element.classList.add('pos-active'));
element.addEventListener('pointerup', () => element.classList.remove('pos-active'));
element.addEventListener('pointerleave', () => element.classList.remove('pos-active'));
```

---

## Responsive Breakpoints

```css
/* Mobile First - Base styles are for mobile */
@media (min-width: 768px) { }   /* Tablet Portrait */
@media (min-width: 1024px) { }  /* Tablet Landscape / Small Desktop */
@media (min-width: 1280px) { }  /* Desktop */
@media (min-width: 1536px) { }  /* Large Desktop / POS Terminal */
```

---

## Device-Specific CSS

```css
.pos-interactive {
  -webkit-user-select: none;
  user-select: none;
  -webkit-touch-callout: none;
  -webkit-tap-highlight-color: transparent;
}

body { overscroll-behavior: none; }
```

---

## Theme System

Theme stored in `localStorage` key `pos-theme`. Toggle via `data-theme` attribute on `<html>`.

```javascript
// Set theme
document.documentElement.setAttribute('data-theme', 'dark');
localStorage.setItem('pos-theme', 'dark');

// Update browser chrome color
document.querySelector('meta[name="theme-color"]')
  ?.setAttribute('content', theme === 'dark' ? '#1e1e2e' : '#eff1f5');
```
