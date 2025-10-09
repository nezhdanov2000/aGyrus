/**
 * Popup Menu Component
 * Reusable menu component for all pages
 */
class PopupMenu {
    constructor(options = {}) {
        this.options = {
            menuBtnId: 'menuBtn',
            closeMenuBtnId: 'closeMenuBtn',
            popupMenuId: 'popupMenu',
            menuOverlayId: 'menuOverlay',
            onSectionChange: null,
            ...options
        };
        
        this.isOpen = false;
        this.init();
    }
    
    init() {
        this.menuBtn = document.getElementById(this.options.menuBtnId);
        this.closeMenuBtn = document.getElementById(this.options.closeMenuBtnId);
        this.popupMenu = document.getElementById(this.options.popupMenuId);
        this.menuOverlay = document.getElementById(this.options.menuOverlayId);
        this.menuItems = document.querySelectorAll('.menu-item');
        
        if (!this.menuBtn || !this.popupMenu) {
            console.warn('PopupMenu: Required elements not found');
            return;
        }
        
        this.bindEvents();
    }
    
    bindEvents() {
        // Open menu
        this.menuBtn.addEventListener('click', () => this.open());
        
        // Close menu
        if (this.closeMenuBtn) {
            this.closeMenuBtn.addEventListener('click', () => this.close());
        }
        
        if (this.menuOverlay) {
            this.menuOverlay.addEventListener('click', () => this.close());
        }
        
        // Handle menu item clicks
        this.menuItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleMenuItemClick(item);
            });
        });
        
        // Handle escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });
    }
    
    open() {
        this.popupMenu.classList.add('open');
        if (this.menuOverlay) {
            this.menuOverlay.classList.add('active');
        }
        document.body.style.overflow = 'hidden';
        this.isOpen = true;
    }
    
    close() {
        this.popupMenu.classList.remove('open');
        if (this.menuOverlay) {
            this.menuOverlay.classList.remove('active');
        }
        document.body.style.overflow = '';
        this.isOpen = false;
    }
    
    handleMenuItemClick(item) {
        console.log('🖱️ Menu item clicked:', item);
        
        // Remove active class from all items
        this.menuItems.forEach(i => i.classList.remove('active'));
        
        // Add active class to clicked item
        item.classList.add('active');
        
        // Get section data
        const section = item.dataset.section;
        console.log('📋 Section:', section);
        
        // Call custom handler if provided
        if (this.options.onSectionChange && typeof this.options.onSectionChange === 'function') {
            console.log('🔧 Using custom handler');
            this.options.onSectionChange(section, item);
        } else {
            console.log('🔧 Using default navigation');
            // Default navigation if no custom handler
            this.handleDefaultNavigation(section);
        }
        
        // Close menu after selection
        this.close();
    }
    
    // Default navigation logic
    handleDefaultNavigation(section) {
        const currentPage = this.getCurrentPage();
        console.log(`🧭 Navigation: ${section} (current page: ${currentPage})`);
        
        switch(section) {
            case 'personal':
                if (currentPage !== 'personal') {
                    console.log('➡️ Navigating to personal.html');
                    window.location.href = 'personal.html';
                } else {
                    console.log('📍 Already on personal page');
                }
                break;
            case 'calendar':
                if (currentPage !== 'calendar') {
                    console.log('➡️ Navigating to calendar.html');
                    window.location.href = 'calendar.html';
                } else {
                    console.log('📍 Already on calendar page');
                }
                break;
            case 'find-tutors':
                if (currentPage !== 'find-tutors') {
                    console.log('➡️ Navigating to find-tutors.html');
                    window.location.href = 'find-tutors.html';
                } else {
                    console.log('📍 Already on find-tutors page');
                }
                break;
            case 'my-tutors':
                if (currentPage !== 'my-tutors') {
                    console.log('➡️ Navigating to my-tutors.html');
                    window.location.href = 'my-tutors.html';
                } else {
                    console.log('📍 Already on my-tutors page');
                }
                break;
            case 'ai':
                if (currentPage !== 'chat') {
                    console.log('➡️ Navigating to chat.html');
                    window.location.href = 'chat.html';
                } else {
                    console.log('📍 Already on chat page');
                }
                break;
            default:
                console.warn(`⚠️ Unknown section: ${section}`);
        }
    }
    
    // Get current page name
    getCurrentPage() {
        const path = window.location.pathname;
        const filename = path.split('/').pop().replace('.html', '');
        return filename;
    }
    
    // Public methods for external control
    setActiveSection(section) {
        this.menuItems.forEach(item => {
            item.classList.remove('active');
            if (item.dataset.section === section) {
                item.classList.add('active');
            }
        });
    }
    
    getActiveSection() {
        const activeItem = document.querySelector('.menu-item.active');
        return activeItem ? activeItem.dataset.section : null;
    }
    
    // Destroy method for cleanup
    destroy() {
        if (this.menuBtn) {
            this.menuBtn.removeEventListener('click', this.open);
        }
        if (this.closeMenuBtn) {
            this.closeMenuBtn.removeEventListener('click', this.close);
        }
        if (this.menuOverlay) {
            this.menuOverlay.removeEventListener('click', this.close);
        }
        document.removeEventListener('keydown', this.handleEscape);
    }
}

// Load menu HTML component
async function loadMenuComponent() {
    const container = document.getElementById('menu-container');
    if (!container) {
        console.warn('Menu container not found');
        return;
    }
    
    console.log('🔄 Loading menu component...');
    
    try {
        const response = await fetch('../components/menu/menu.html');
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        const html = await response.text();
        container.innerHTML = html;
        
        console.log('✅ Menu HTML loaded successfully');
        
        // Initialize menu after HTML is loaded
        if (document.getElementById('popupMenu') && document.getElementById('menuBtn')) {
            window.popupMenu = new PopupMenu();
            console.log('✅ Menu initialized after HTML load');
        } else {
            console.warn('⚠️ Menu elements not found after HTML load');
        }
    } catch (error) {
        console.error('❌ Failed to load menu component:', error);
        console.log('🔄 Trying fallback initialization...');
        
        // Fallback: try to initialize with existing elements
        if (document.getElementById('popupMenu') && document.getElementById('menuBtn')) {
            window.popupMenu = new PopupMenu();
            console.log('✅ Menu initialized via fallback');
        }
    }
}

// Auto-initialize if menu elements exist
document.addEventListener('DOMContentLoaded', function() {
    // Try to load menu component first
    loadMenuComponent();
    
    // Fallback: initialize if elements already exist
    if (document.getElementById('popupMenu') && document.getElementById('menuBtn')) {
        window.popupMenu = new PopupMenu();
    }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PopupMenu;
}
