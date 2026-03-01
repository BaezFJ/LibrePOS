/**
 * Flash Messages Module
 * Displays flash messages and announces them to screen readers
 */

const initFlashMessages = () => {
    const container = document.getElementById('flash-messages-data');
    const announcer = document.getElementById('flash-announcer');

    if (!container) return;

    const messages = JSON.parse(container.dataset.messages || '[]');

    messages.forEach(({ category, message }) => {
        // TODO: Implement BeerCSS snackbar notifications
        console.log(`[${category.toUpperCase()}] ${message}`);

        // Announce to screen readers
        if (announcer) {
            announcer.textContent = `${category}: ${message}`;
        }
    });
};

document.addEventListener('DOMContentLoaded', initFlashMessages);
