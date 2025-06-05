document.addEventListener('DOMContentLoaded', function () {
    // nav menu
    const menus = document.querySelectorAll('.side-menu');
    M.Sidenav.init(menus, {edge: 'right'});
    // add recipe form
    const forms = document.querySelectorAll('.side-form');
    M.Sidenav.init(forms, {edge: 'left'});
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