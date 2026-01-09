// Helper functions for the application

/**
 * Appends the button's value to an input field
 * @param {HTMLButtonElement} button - The button element containing the value
 * @param {string} inputID - The ID of the input element
 */
function addToInput(button, inputID) {
    const inputElement = document.getElementById(inputID);
    inputElement.value += button.value;
}

/**
 * Clears the value of an input field
 * @param {string} inputID - The ID of the input element
 */
function clearInput(inputID) {
    const inputElement = document.getElementById(inputID);
    inputElement.value = '';
}

/**
 * Deletes the last character from an input field
 * @param {string} inputID - The ID of the input element
 */
function deleteLastChar(inputID) {
    const inputElement = document.getElementById(inputID);
    inputElement.value = inputElement.value.slice(0, -1);
}

/**
 * Increments the numeric value of an input field by 1
 * @param {string} inputID - The ID of the input element
 */
function incrementValue(inputID) {
    const inputField = document.getElementById(inputID);
    const currentValue = parseInt(inputField.value, 10);
    inputField.value = currentValue + 1;
}

/**
 * Decrements the numeric value of an input field by 1 (minimum value: 1)
 * @param {string} inputID - The ID of the input element
 */
function decrementValue(inputID) {
    const inputField = document.getElementById(inputID);
    const currentValue = parseInt(inputField.value, 10);

    // Check if the current value is greater than 1 before decreasing
    if (currentValue > 1) {
        inputField.value = currentValue - 1;
    } else {
        inputField.value = 1; // Ensure the value stays at 1 if it reaches the limit
    }
}

/**
 * Initialize all file dropzones on the page
 * Adds drag-and-drop functionality and click-to-browse
 */
function initFileDropzones() {
    document.querySelectorAll('.file-dropzone').forEach(zone => {
        const input = zone.querySelector('.file-dropzone__input');
        const preview = zone.querySelector('.file-dropzone__preview');

        if (!input) return;

        // Click anywhere in zone to open file browser
        zone.addEventListener('click', (e) => {
            if (e.target !== input) {
                input.click();
            }
        });

        // Drag enter - add visual feedback
        zone.addEventListener('dragenter', (e) => {
            e.preventDefault();
            zone.classList.add('file-dropzone--dragover');
        });

        // Drag over - required to allow drop
        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('file-dropzone--dragover');
        });

        // Drag leave - remove visual feedback
        zone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            zone.classList.remove('file-dropzone--dragover');
        });

        // Drop - handle dropped files
        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('file-dropzone--dragover');

            if (e.dataTransfer.files.length > 0) {
                input.files = e.dataTransfer.files;
                updateFilePreview(preview, input.files);
                // Trigger change event for form validation
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
        });

        // Native file selection via input
        input.addEventListener('change', () => {
            updateFilePreview(preview, input.files);
        });
    });
}

/**
 * Updates the preview element with the selected file name(s)
 * @param {HTMLElement} previewEl - The preview element to update
 * @param {FileList} files - The selected files
 */
function updateFilePreview(previewEl, files) {
    if (!previewEl) return;

    if (files.length === 0) {
        previewEl.textContent = '';
    } else if (files.length === 1) {
        previewEl.textContent = files[0].name;
    } else {
        previewEl.textContent = `${files.length} files selected`;
    }
}

// Auto-initialize dropzones when DOM is ready
document.addEventListener('DOMContentLoaded', initFileDropzones);
