document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');

    // Обработчик отправки формы логина
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();  // Предотвратить отправку формы по умолчанию

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        const formData = {
            username: username,
            password: password
        };

        fetch('/api/admin/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Ответ от сервера:', data);
            if (data.access_token) {
                // Сохраняем токен в localStorage
                localStorage.setItem('jwt_token', data.access_token);
                window.location.href = 'http://127.0.0.1:5000/visualization/';  // Переход на главную страницу после входа
            } else {
                alert('Неверные данные для входа.');
            }
        })
        .catch(error => {
            console.error('Ошибка при входе:', error);
        });
    });
});
