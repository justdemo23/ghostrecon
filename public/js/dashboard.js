document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    const errorMessage = document.getElementById('errorMessage');

    if (!token) {
        window.location.href = '/login';
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

        document.getElementById('username').textContent = data.usuario.nombre;
    } catch (error) {
        localStorage.removeItem('token');
        window.location.href = '/login';
    }
});

document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('token');
    window.location.href = '/public/home.html';
});




