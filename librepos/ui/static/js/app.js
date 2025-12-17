// Constants
const SERVICE_WORKER_SCRIPT = '/sw.js';
const SERVICE_WORKER_SUCCESS_MSG = '--- Service Worker registered successfully ---';
const SERVICE_WORKER_ERROR_MSG = '*** Service Worker registration failed ***';
// Selector constants
const TAB_SELECTOR = '.tabs';
const TAB_CONTENT_SELECTOR = (selectedTabId) => `#${selectedTabId}-content`;

// Service worker registration logic
const registerServiceWorker = () => {
    navigator.serviceWorker
        .register(SERVICE_WORKER_SCRIPT)
        .then(() => console.log(SERVICE_WORKER_SUCCESS_MSG))
        .catch(error => console.error(SERVICE_WORKER_ERROR_MSG, error));
};

// Service worker registration check
// TODO: Service worker not re-caching after auth logout. (temp disable)
// if ('serviceWorker' in navigator) {
//     window.addEventListener("load", () => registerServiceWorker());
// }


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


function addToInput(button, inputID) {
    const inputElement = document.getElementById(inputID);
    inputElement.value += button.value;
}

function clearInput(inputID) {
    const inputElement = document.getElementById(inputID);
    inputElement.value = '';
}

function deleteLastChar(inputID) {
    const inputElement = document.getElementById(inputID);
    inputElement.value = inputElement.value.slice(0, -1);
}

function incrementValue(inputID) {
    const inputField = document.getElementById(inputID);
    const currentValue = parseInt(inputField.value, 10);
    inputField.value = currentValue + 1;
}

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