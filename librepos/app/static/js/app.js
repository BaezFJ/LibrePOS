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
    const sidenavElements = document.querySelectorAll('.sidenav');

    // Function to initialize a single sidenav instance
    const initializeRightSidenav = (element) => {
        const edge = element.classList.contains('right') ? 'right' : 'left';
        M.Sidenav.init(element, {edge});
    };

    // Initialize each sidenav element
    sidenavElements.forEach(initializeRightSidenav);

    // Function to initialize collapsible
    const initializeCollapsible = () => {
        const collapsibleElements = document.querySelectorAll('.collapsible');
        M.Collapsible.init(collapsibleElements);
    };

    // Initialize collapsible
    initializeCollapsible();

    // Modal configuration options
    const modalOptions = {
        inDuration: 150, outDuration: 150, opacity: 1,
    };

    // Function to initialize modals
    const initializeModals = () => {
        const modalElements = document.querySelectorAll('.modal');
        const modalInstances = M.Modal.init(modalElements, modalOptions);
        return modalInstances;
    };

    // Initialize modals
    initializeModals();

    // Function to handle the 'onShow' event
    const handleTabShow = (tab) => {
        const selectedTabId = tab.getAttribute('id');
        const tabContent = document.querySelector(TAB_CONTENT_SELECTOR(selectedTabId));
        if (tabContent) {
            tabContent.classList.add('active');
        }
    };

    // Function to initialize tabs
    const initializeTabs = () => {
        const tabs = document.querySelectorAll(TAB_SELECTOR);
        return M.Tabs.init(tabs, {
            swipeable: true,
            onShow: handleTabShow,
            duration: 200,
        });
    };

    // Initialize tabs
    initializeTabs();

    const initializeSelectElements = () => {
        const selectElements = document.querySelectorAll('select');
        return M.FormSelect.init(selectElements, {
            // Specify options here
        });
    };

    // Initialize select elements
    initializeSelectElements();

    // M.Forms.InitFileInputPath(document.querySelector('.file-input'));

    // Const for calculating dates based on working age.
    const CURRENT_DATE = new Date();
    const MIN_WORKING_AGE = 12;
    const MAX_WORKING_AGE = 65;

    // Calculated important dates based on ages.
    const MAX_WORKING_YEAR = CURRENT_DATE.getFullYear() - MIN_WORKING_AGE;
    const MIN_WORKING_YEAR = CURRENT_DATE.getFullYear() - MAX_WORKING_AGE;


    // Function to initialize date picker
    const initializeDatepicker = () => {
        const datepickerElements = document.querySelectorAll('.datepicker');
        return M.Datepicker.init(datepickerElements, {
            autoClose: true,
            format: 'yyyy-mm-dd', // Example: Set the date format (1990-12-01)
            yearRange: [MIN_WORKING_YEAR, MAX_WORKING_YEAR],
            yearRangeReverse: true,
            showClearBtn: true,
            i18n: {
                done: "Select"
            }
        });
    };

    // Initialize datepicker
    initializeDatepicker();

    // Function to initialize tooltips
    const initializeTooltips = () => {
        const tooltipElements = document.querySelectorAll('.tooltipped');
        return M.Tooltip.init(tooltipElements, {
            // Tooltip options can be specified here
            // enterDelay: 200,
            // exitDelay: 100,
            // etc.
        });
    };

    // Initialize tooltips
    initializeTooltips();

    // Dropdowns
    const dropdownTriggerSelector = '.dropdown-trigger';
    const dropdownOptions = {
        // specify options here
        constrainWidth: false, // don't force dropdown to avatar width
        coverTrigger: false,   // show dropdown below the avatar
        alignment: 'right'     // align menu to the right edge of avatar
    };

    const initializeDropdowns = () => {
        const dropdownTriggerElements = document.querySelectorAll(dropdownTriggerSelector);
        const dropdownInstances = M.Dropdown.init(dropdownTriggerElements, dropdownOptions);
        return dropdownInstances;
    };

    // Initialize dropdowns
    initializeDropdowns();


});