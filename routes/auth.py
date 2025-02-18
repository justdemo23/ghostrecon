from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
import bcrypt
import jwt
import datetime
from db import get_db_connection

# 📌 Clave secreta para firmar los tokens JWT (¡Cámbiala por algo seguro en producción!)
SECRET_KEY = "TJksAUKpANGW69wuUuCKsaAUmggcCgz2nr"

router = APIRouter()

# 📌 Modelos para validación de datos con Pydantic
class UsuarioRegistro(BaseModel):
    nombre: str
    email: str
    password: str

class UsuarioLogin(BaseModel):
    email: str
    password: str

# 📌 Función para generar un JWT (Expira en 24 horas)
def generar_token(email):
    payload = {
        "sub": email,  
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)  
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# 📌 Función para verificar y decodificar el token JWT
def verificar_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token no encontrado")

    token = authorization.split("Bearer ")[-1]  # Extrae el token del header

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]  # Retorna el email del usuario autenticado
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

# 📌 Ruta para registrar usuarios
@router.post("/register", status_code=201)
async def register(user: UsuarioRegistro):
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", 
                       (user.nombre, user.email, hashed_password))
        conn.commit()
        return {"mensaje": "Usuario registrado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# 📌 Ruta para login con JWT
@router.post("/login", status_code=200)
async def login(user: UsuarioLogin):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (user.email,))
    usuario = cursor.fetchone()

    if usuario is None:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if bcrypt.checkpw(user.password.encode("utf-8"), usuario["password"].encode("utf-8")):
        token = generar_token(user.email)  # Generamos el token JWT
        return {"mensaje": "Inicio de sesión exitoso", "token": token}
    else:
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

# 📌 Ruta protegida con JWT (Solo accede si el token es válido)
@router.get("/me")
async def obtener_usuario(email: str = Depends(verificar_token)):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT nombre, email FROM usuarios WHERE email = %s", (email,))
    usuario = cursor.fetchone()

    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"usuario": usuario}

