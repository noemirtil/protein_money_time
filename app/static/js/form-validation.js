    
function checkPasswordsMatch() {
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirm_password');
    const messageDiv = document.getElementById('password-match-message');

    confirmPasswordField.addEventListener('input', function() {

        const password = passwordField.value;
        const confirmPassword = confirmPasswordField.value;

        if (confirmPassword === '') {
            messageDiv.textContent = '';
            messageDiv.className = 'mt-1 text-sm';
        } else if (password === confirmPassword) {
            messageDiv.textContent = '✅ Las contraseñas coinciden.';
            messageDiv.className = 'mt-1 text-sm text-green-700';
        } else {
            messageDiv.textContent = '❌ Las contraseñas no coinciden.';
            messageDiv.className = 'mt-1 text-sm text-red-700';
        }
    });

    passwordField.addEventListener('input', function() {
        confirmPasswordField.dispatchEvent(new Event('input'));
    });
}

function checkPasswordValidity() {
    const passwordField = document.getElementById('password');
    const messageDiv = document.getElementById('password-validation-message');

    passwordField.addEventListener('input', function() {

        const password = passwordField.value;

        if (password.length === 0) {
            messageDiv.textContent = '';
            messageDiv.className = 'mt-1 text-sm';
        } else if (password.length >= 5) {
            messageDiv.textContent = '✅ La contraseña es válida.';
            messageDiv.className = 'mt-1 text-sm text-green-700';
        } else {
            messageDiv.textContent = '❌ Contraseña inválida.';
            messageDiv.className = 'mt-1 text-sm text-red-700';
        }
    });
}

function checkUsernameAvailability() {
    const usernameField = document.getElementById('username');
    const messageDiv = document.getElementById('username-message');
    let timeoutId = null;

    usernameField.addEventListener('input', function() {

        const username = usernameField.value.trim().toLowerCase();

        clearTimeout(timeoutId);

        if (username === '') {
            messageDiv.textContent = '';
            return;
        }

        if (username.length < 3) {
            messageDiv.textContent = 'ℹ️ Mínimo 3 caracteres';
            messageDiv.className = 'mt-1 text-sm text-blue-600';
            return;
        }

        messageDiv.textContent = '⏳ Verificando...';
        messageDiv.className = 'mt-1 text-sm text-gray-600';

        timeoutId = setTimeout(function() {
            fetch('/auth/check-username?username=' + username).then(response => response.json()).then(data => {
                if (data.available) {
                    messageDiv.textContent = '✅ Nombre de usuario disponible.';
                    messageDiv.className = 'mt-1 text-sm text-green-700';
                } else {
                    messageDiv.textContent = '❌ Nombre de usuario no disponible.';
                    messageDiv.className = 'mt-1 text-sm text-red-700';
                }
            }).catch(error => {
                messageDiv.textContent = '❌ Error al verificar.';
                messageDiv.className = 'mt-1 text-sm text-red-700';
            });
        }, 500);
    });
}

function checkEmailAvailability() {

    const emailField = document.getElementById('email');
    const messageDiv = document.getElementById('email-message');
    let timeoutId = null;

    emailField.addEventListener('input', function() {

        const email = emailField.value.trim().toLowerCase();

        clearTimeout(timeoutId);

        if (email === '') {
            messageDiv.textContent = '';
            return;
        }

        if (email.length <= 3) {
            messageDiv.textContent = 'ℹ️ Mínimo 3 caracteres';
            messageDiv.className = 'mt-1 text-sm text-blue-600';
            return;
        }

        if (!email.includes('@') || !email.includes('.')) {
            messageDiv.textContent = 'ℹ️ E-mail no válido.';
            messageDiv.className = 'mt-1 text-sm text-blue-600';
            return;
        }

        messageDiv.textContent = '⏳ Verificando...';
        messageDiv.className = 'mt-1 text-sm text-gray-600';

        timeoutId = setTimeout(function() {
            fetch('/auth/check-email?email=' + email).then(response => response.json()).then(data => {
                if (data.available) {
                    messageDiv.textContent = '✅ E-mail disponible.';
                    messageDiv.className = 'mt-1 text-sm text-green-700';
                } else {
                    messageDiv.textContent = '❌ E-mail no disponible.';
                    messageDiv.className = 'mt-1 text-sm text-red-700';
                }
            }).catch(error => {
                messageDiv.textContent = '❌ Error al verificar.';
                messageDiv.className = 'mt-1 text-sm text-red-700';
            });
        }, 500);
    });
}

checkPasswordsMatch();
checkPasswordValidity();
checkUsernameAvailability();
checkEmailAvailability();