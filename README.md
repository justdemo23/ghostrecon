# FaceID Pro - Sistema de Reconocimiento Facial

## Descripción
FaceID Pro es un sistema de reconocimiento facial que permite registrar y consultar personas mediante el análisis de sus rostros. El sistema utiliza tecnología avanzada de reconocimiento facial para identificar y verificar la identidad de las personas.

## Características Principales
- Registro de usuarios con autenticación JWT
- Registro de personas con información personal y reconocimiento facial
- Consulta de personas mediante reconocimiento facial
- Interfaz web intuitiva
- Base de datos MySQL para almacenamiento seguro

## Tecnologías Utilizadas
- **Backend:**
  - FastAPI (Framework web de Python)
  - face_recognition (Biblioteca de reconocimiento facial)
  - MySQL (Base de datos)
  - JWT (Autenticación de usuarios)
  - bcrypt (Encriptación de contraseñas)

- **Frontend:**
  - HTML/CSS
  - JavaScript

## Requisitos de Instalación
1. Python 3.x
2. MySQL
3. Dependencias de Python (instalar con pip):
```python
pip install -r requirements.txt
```

## Estructura de la Base de Datos
### Tabla `usuarios`
- id (INT, AUTO_INCREMENT, PRIMARY KEY)
- nombre (VARCHAR)
- email (VARCHAR, UNIQUE)
- password (VARCHAR)
- created_at (TIMESTAMP)

### Tabla `personas`
- id (INT, AUTO_INCREMENT, PRIMARY KEY)
- nombre (VARCHAR)
- apellido (VARCHAR)
- direccion (TEXT)
- fecha_nacimiento (DATE)
- telefono (VARCHAR)
- cedula (VARCHAR, UNIQUE)
- codificacion_facial (LONGBLOB)
- created_at (TIMESTAMP)

## Configuración
1. Crear la base de datos MySQL:
```sql
CREATE DATABASE reconocimiento_facial;
```

2. Configurar las credenciales de la base de datos en el archivo de configuración:
```python
host="localhost"
user="root"
password="tu_contraseña"
database="reconocimiento_facial"
```

## Endpoints de la API
### Autenticación
- POST `/auth/register` - Registro de usuarios
- POST `/auth/login` - Inicio de sesión
- GET `/auth/me` - Información del usuario actual

### Reconocimiento Facial
- POST `/reconocimiento/registrar` - Registrar nueva persona con foto
- POST `/reconocimiento/consultar` - Consultar persona mediante foto

## Uso
1. Iniciar el servidor:
```bash
python api.py
```
2. Acceder a la aplicación web en: 