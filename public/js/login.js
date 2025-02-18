document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('errorMessage');

    try {
        const response = await fetch('http://127.0.0.1:3100/auth/login', {  // 🔥 Conexión directa al backend
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Error en el inicio de sesión'); // 🔥 Corrige manejo de errores
        }

        // Guardar token en localStorage para usarlo en futuras peticiones
        localStorage.setItem('token', data.token);

        // Redirigir al usuario al dashboard
        window.location.href = '/public/dashboard.html';
        
    } catch (error) {
        errorMessage.style.display = 'block';
        errorMessage.textContent = error.message;
    }
});
