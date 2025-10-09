# Popup Menu Component

Reusable popup menu component for all pages in the Gyrus AI project.

## Files Structure

```
components/menu/
├── menu.html      # HTML structure
├── menu.css       # Styles
├── menu.js        # JavaScript functionality
└── README.md      # Documentation
```

## Usage

### 1. Include CSS and JS files

```html
<head>
    <link rel="stylesheet" href="../components/menu/menu.css">
    <script src="../components/menu/menu.js"></script>
</head>
<body>
    <!-- Your page content -->
    
    <!-- Menu container -->
    <div id="menu-container"></div>
</body>
```

### 2. Add menu button to your header

```html
<header class="app-header">
    <button class="icon-btn" id="menuBtn" aria-label="Menu" title="Menu">
        <span class="icon">☰</span>
    </button>
    <!-- Rest of your header -->
</header>
```

### 3. Initialize with custom handler (optional)

```javascript
// Custom menu section handler
function handleMenuSection(section) {
    switch(section) {
        case 'personal':
            // Handle personal data
            break;
        case 'calendar':
            // Handle calendar
            break;
        case 'find-tutors':
            // Handle tutor search
            break;
        case 'my-tutors':
            // Handle my tutors
            break;
        case 'ai':
            // Handle AI
            break;
    }
}

// Initialize menu with custom handler (after DOM is ready)
document.addEventListener('DOMContentLoaded', function() {
    if (window.PopupMenu) {
        window.popupMenu = new PopupMenu({
            onSectionChange: handleMenuSection
        });
    }
});
```

## API

### PopupMenu Class

#### Constructor Options

```javascript
new PopupMenu({
    menuBtnId: 'menuBtn',           // ID of menu button
    closeMenuBtnId: 'closeMenuBtn', // ID of close button
    popupMenuId: 'popupMenu',       // ID of popup menu
    menuOverlayId: 'menuOverlay',   // ID of overlay
    onSectionChange: null           // Custom section handler
})
```

#### Methods

- `open()` - Open the menu
- `close()` - Close the menu
- `setActiveSection(section)` - Set active menu section
- `getActiveSection()` - Get current active section
- `destroy()` - Clean up event listeners

## Menu Sections

- `personal` - Personal data management
- `calendar` - Calendar view
- `find-tutors` - Find tutors
- `my-tutors` - My tutors/bookings
- `ai` - AI Assistant

## Styling

The component uses CSS custom properties for theming:

```css
:root {
    --white: #fff;
    /* Add your custom properties */
}
```

## Responsive Design

- **Desktop (>768px)**: 280px width, slides from left
- **Mobile (≤768px)**: Full width (100%), slides from top
- **Small mobile (≤480px)**: Optimized spacing and font sizes

## Browser Support

- Modern browsers with ES6+ support
- Fetch API support required for HTML loading
