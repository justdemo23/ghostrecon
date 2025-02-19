document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    const errorMessage = document.getElementById('errorMessage');

    if (!token) {
        window.location.href = '/login'; // 🔥 Si no hay token, redirigir al login
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:3100/auth/me', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'No autorizado');
        }

        // Mostrar datos del usuario en el dashboard
        document.getElementById('username').textContent = data.usuario.nombre;
    } catch (error) {
        localStorage.removeItem('token'); // 🔥 Si hay error, limpiar el token
        window.location.href = '/login';
    }
});

// clic en boton de cerrar sesion en el dashboard.html <button id="logoutBtn">Cerrar Sesión</button>
document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('token');
    window.location.href = '/public/home.html';
});




