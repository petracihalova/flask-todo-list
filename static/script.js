function togglePasswordVisibility(passwordFieldId) {
    const passwordField = document.getElementById(passwordFieldId);
    const isPasswordVisible = passwordField.type === "text";
    passwordField.type = isPasswordVisible ? "password" : "text";

    const eyeIcon = document.getElementById(isPasswordVisible ? "eye-icon-" + passwordFieldId : "eye-icon-" + passwordFieldId);
    eyeIcon.classList.toggle("bi-eye"); // změna na ikonu "oko"
    eyeIcon.classList.toggle("bi-eye-slash"); // změna na ikonu "přeškrtnuté oko"
};

const password = document.querySelector('#password');
const confirmPassword = document.querySelector('#confirm-password');
const form = document.querySelector('#register-form');

// Zkontrolujeme, zda jsou hesla stejná při odeslání formuláře
form.addEventListener('submit', function (event) {
    if (password.value !== confirmPassword.value) {
        event.preventDefault(); // Zabrání odeslání formuláře
        password.classList.add('is-invalid');
        confirmPassword.classList.add('is-invalid');
    } else {
        password.classList.remove('is-invalid');
        confirmPassword.classList.remove('is-invalid');
    }
});

// Zkontrolujeme hesla i při psaní
confirmPassword.addEventListener('input', function () {
    if (password.value !== confirmPassword.value) {
        confirmPassword.classList.add('is-invalid');
    } else {
        confirmPassword.classList.remove('is-invalid');
    }
});
