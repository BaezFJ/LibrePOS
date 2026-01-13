// Selector constants
const TAB_SELECTOR = '.tabs';
const TAB_CONTENT_SELECTOR = (selectedTabId) => `#${selectedTabId}-content`;

// PWA utilities - provides service worker management and cache control
const PWA = {
    registration: null,
    updateAvailable: false,

    // Register service worker with update detection
    async register() {
        if (!('serviceWorker' in navigator)) {
            console.warn('[PWA] Service Workers not supported');
            return null;
        }

        try {
            this.registration = await navigator.serviceWorker.register('/sw.js', {
                scope: '/',
            });
            console.log('[PWA] Service Worker registered successfully');

            // Check for updates
            this.registration.addEventListener('updatefound', () => {
                const newWorker = this.registration.installing;
                if (newWorker) {
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            console.log('[PWA] New service worker available');
                            this.updateAvailable = true;
                            window.dispatchEvent(new CustomEvent('pwa:update-available'));
                        }
                    });
                }
            });

            return this.registration;
        } catch (error) {
            console.error('[PWA] Service Worker registration failed:', error);
            return null;
        }
    },

    // Clear all caches - call this on logout to fix stale cache issue
    async clearCaches() {
        if (!navigator.serviceWorker.controller) {
            console.warn('[PWA] No active service worker to clear caches');
            return false;
        }

        return new Promise((resolve, reject) => {
            const messageChannel = new MessageChannel();
            const timeout = setTimeout(() => {
                reject(new Error('[PWA] Cache clear timeout'));
            }, 5000);

            messageChannel.port1.onmessage = (event) => {
                clearTimeout(timeout);
                if (event.data && event.data.type === 'CACHES_CLEARED') {
                    console.log('[PWA] All caches cleared');
                    resolve(true);
                }
            };

            navigator.serviceWorker.controller.postMessage(
                { type: 'CLEAR_CACHES' },
                [messageChannel.port2]
            );
        });
    },

    // Force update to new service worker
    async update() {
        if (this.registration && this.registration.waiting) {
            this.registration.waiting.postMessage({ type: 'SKIP_WAITING' });
        }
    },

    // Check if app is running as installed PWA
    isInstalled() {
        return window.matchMedia('(display-mode: standalone)').matches ||
               window.navigator.standalone === true;
    },
};

// Install prompt handling
let deferredInstallPrompt = null;

window.addEventListener('beforeinstallprompt', (event) => {
    event.preventDefault();
    deferredInstallPrompt = event;
    window.dispatchEvent(new CustomEvent('pwa:install-available'));
});

window.addEventListener('appinstalled', () => {
    deferredInstallPrompt = null;
    console.log('[PWA] App installed');
    window.dispatchEvent(new CustomEvent('pwa:installed'));
});

// Function to show install prompt (call from UI)
window.showInstallPrompt = async () => {
    if (!deferredInstallPrompt) {
        return false;
    }

    deferredInstallPrompt.prompt();
    const { outcome } = await deferredInstallPrompt.userChoice;
    deferredInstallPrompt = null;
    return outcome === 'accepted';
};

// Expose PWA utilities globally
window.PWA = PWA;

// Register service worker on load
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => PWA.register());
}


document.addEventListener('DOMContentLoaded', () => {
    // Bootstrap 5 auto-initializes most components via data-bs-* attributes.
    // Only components that require explicit initialization are handled here.

    // Initialize all tooltips (Bootstrap requires explicit initialization)
    const initializeTooltips = () => {
        const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        return [...tooltipElements].map(el => new bootstrap.Tooltip(el));
    };

    initializeTooltips();

    // Initialize all popovers (Bootstrap requires explicit initialization)
    const initializePopovers = () => {
        const popoverElements = document.querySelectorAll('[data-bs-toggle="popover"]');
        return [...popoverElements].map(el => new bootstrap.Popover(el));
    };

    initializePopovers();

    // Handle tab content activation
    const tabElements = document.querySelectorAll('[data-bs-toggle="tab"]');
    tabElements.forEach(tab => {
        tab.addEventListener('shown.bs.tab', (event) => {
            const selectedTabId = event.target.getAttribute('id');
            const tabContent = document.querySelector(TAB_CONTENT_SELECTOR(selectedTabId));
            if (tabContent) {
                tabContent.classList.add('active');
            }
        });
    });

    // Datepicker: Bootstrap 5 doesn't include a datepicker.
    // Use native HTML5 date input or add a third-party library like Tempus Dominus.
    // For now, datepicker elements use native <input type="date">.
});