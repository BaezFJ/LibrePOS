/**
 * Flash Messages Module
 * Displays flash messages using MaterializeCSS Toast
 * and announces them to screen readers via aria-live region
 */

const initFlashMessages = () => {
    const container = document.getElementById('flash-messages-data');
    const announcer = document.getElementById('flash-announcer');

    if (!container) return;

    const messages = JSON.parse(container.dataset.messages || '[]');

    messages.forEach(({ category, message }) => {
        // Create toast using MaterializeCSS
        M.toast({
            html: `<div class="pos-toast pos-toast--${category}" role="alert">
                <p class="pos-toast-text"><strong>${category.toUpperCase()}:</strong> ${message}</p>
            </div>`
        });

        // Announce to screen readers
        if (announcer) {
            announcer.textContent = `${category}: ${message}`;
        }
    });
};

document.addEventListener('DOMContentLoaded', initFlashMessages);
