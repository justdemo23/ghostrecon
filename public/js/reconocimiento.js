document.getElementById('recognizeBtn').addEventListener('click', async () => {
    const fileInput = document.getElementById('fileInput');
    const resultMessage = document.getElementById('resultMessage');

    if (!fileInput.files.length) {
        resultMessage.textContent = "❌ Por favor, selecciona una imagen.";
        return;
    }
    const formData = new FormData();
    formData.append("imagen", fileInput.files[0]);

    try {
        const response = await fetch("http://127.0.0.1:3100/reconocimiento/consultar", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            if (data.nombre) {
                resultMessage.innerHTML = `
                    <p>✅ Persona encontrada</p>
                    <p><strong>Nombre:</strong> ${data.nombre} ${data.apellido}</p>
                    <p><strong>Cédula:</strong> ${data.cedula}</p>
                    <p><strong>Dirección:</strong> ${data.direccion}</p>
                    <p><strong>Fecha de Nacimiento:</strong> ${data.fecha_nacimiento}</p>
                    <p><strong>Teléfono:</strong> ${data.telefono}</p>
                `;
            } else {
                resultMessage.textContent = "❌ Persona NO encontrada";
            }
        } else {
            resultMessage.textContent = `⚠️ Error: ${data.detail}`;
        }
    } catch (error) {
        console.error("❌ Error:", error);
        resultMessage.textContent = "❌ Error en la solicitud.";
    }
});
