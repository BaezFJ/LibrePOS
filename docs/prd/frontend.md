# Frontend Framework Configuration

> MaterializeCSS, Chart.js, SortableJS, and interact.js integration

---

## Overview

The frontend stack combines MaterializeCSS for consistent Material Design styling with specialized JavaScript libraries for interactive features. This approach provides a polished, professional appearance while enabling complex interactions required for POS operations.

---

## MaterializeCSS - Base Styling

MaterializeCSS serves as the base styling framework, providing Material Design components optimized for touch interfaces.

- Material Design components: cards, buttons, forms, modals, navigation
- Responsive grid system with 12-column layout
- Built-in JavaScript components: dropdowns, modals, tabs, toasts
- Touch-optimized interactions for mobile and tablet devices
- Color palette system with primary, secondary, and status colors
- Typography scale and spacing utilities

---

## Chart.js - Data Visualization

Chart.js provides flexible, responsive charting capabilities for reporting and analytics.

| Chart Type | Use Cases |
|------------|-----------|
| Line Charts | Sales trends, hourly patterns, year-over-year comparisons |
| Bar Charts | Sales by category, server performance, day-of-week analysis |
| Doughnut/Pie | Payment distribution, product mix, labor cost breakdown |
| Mixed Charts | Revenue vs covers overlay, sales vs labor correlation |

---

## SortableJS - Drag-and-Drop Reordering

SortableJS enables intuitive drag-and-drop reordering for list-based management interfaces.

| Feature Area | Implementation |
|--------------|----------------|
| Menu Item Reordering | Drag items within categories, drag between categories |
| Category Management | Reorder categories, nest subcategories |
| Modifier Group Ordering | Set modifier group sequence, reorder modifiers |
| Course Sequencing | Drag items between courses |
| Station Assignment | Drag categories to kitchen stations |

---

## interact.js - Floor Plan Editor

interact.js powers the visual floor plan editor for table management.

| Capability | Description |
|------------|-------------|
| Free Dragging | Position tables anywhere on the canvas |
| Snap to Grid | Optional grid snapping for aligned layouts |
| Table Resizing | Resize combined tables for merged seating |
| Rotation | Rotate tables (45-degree increments) |
| Boundary Constraints | Keep tables within floor plan boundaries |
| Multi-Select | Select and move multiple tables simultaneously |

---

## File Structure

```
app/static/vendor/          # MaterializeCSS, Chart.js, SortableJS, interact.js
app/static/css/main.css     # Global custom styles
app/static/js/app.js        # Global JavaScript initialization
blueprints/{name}/static/   # Blueprint-specific CSS and JavaScript
```

---

## Theme Customization

MaterializeCSS is customized via Sass variables for consistent brand identity.

| Token | Purpose |
|-------|---------|
| `$primary-color` | Navigation, buttons, interactive elements |
| `$secondary-color` | Highlights and secondary actions |
| `$success-color` | Completed orders, available tables, successful payments |
| `$error-color` | Voided items, payment failures, allergy warnings |
| `$warning-color` | Late tickets, low stock alerts, expiring items |
| `$info-color` | Rush orders, VIP tables, special instructions |

---

## Template Engine Configuration

### Jinja2 Extensions

- `jinja2.ext.do` - Execute statements within templates
- `jinja2.ext.loopcontrols` - Enable break and continue in loops
- `jinja2.ext.debug` - Debug output in development mode only

### Custom Filters

| Filter | Purpose |
|--------|---------|
| `currency` | Format monetary values |
| `timeago` | Display relative timestamps |
| `pluralize` | Smart pluralization for counts |
| `status_badge` | Generate HTML badges for statuses |

### Global Context Processors

| Processor | Purpose |
|-----------|---------|
| `current_location` | Active restaurant location |
| `current_shift` | Active shift information |
| `permissions` | User permission set for conditional UI |
