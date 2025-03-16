from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
import face_recognition
import numpy as np
import os
from db import get_db_connection
from routes.auth import verificar_token
from datetime import datetime

router = APIRouter()

UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

def guardar_persona(nombre, apellido, direccion, fecha_nacimiento, telefono, cedula, codificacion_facial):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO personas (nombre, apellido, direccion, fecha_nacimiento, telefono, cedula, codificacion_facial) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, direccion, fecha_nacimiento, telefono, cedula, codificacion_facial.tobytes()))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al guardar persona: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def guardar_imagen_temp(file: UploadFile):
    file_path = os.path.join(UPLOADS_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return file_path

def procesar_imagen(file_path):
    try:
        image = face_recognition.load_image_file(file_path)
        codificaciones = face_recognition.face_encodings(image)
        if len(codificaciones) == 0:
            raise HTTPException(status_code=400, detail="No se detectó ningún rostro en la imagen.")

        return codificaciones[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post("/registrar")
async def registrar_persona(
    nombre: str = Form(...),
    apellido: str = Form(...),
    direccion: str = Form(...),
    fecha_nacimiento: str = Form(...),
    telefono: str = Form(...),
    cedula: str = Form(...),
    imagen: UploadFile = File(...),
    usuario_email: str = Depends(verificar_token)
):
    try:
        file_path = guardar_imagen_temp(imagen)
        codificacion_facial = procesar_imagen(file_path)

        guardar_persona(nombre, apellido, direccion, fecha_nacimiento, telefono, cedula, codificacion_facial)

        return {"mensaje": "Persona registrada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar persona: {str(e)}")

def obtener_persona_por_codificacion(codificacion_facial):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM personas")
    personas = cursor.fetchall()
    cursor.close()
    conn.close()

    for persona in personas:
        codificacion_guardada = np.frombuffer(persona["codificacion_facial"])  
        coincide = face_recognition.compare_faces([codificacion_guardada], codificacion_facial)[0]
        if coincide:
            return {
                "nombre": persona["nombre"],
                "apellido": persona["apellido"],
                "direccion": persona["direccion"],
                "fecha_nacimiento": str(persona["fecha_nacimiento"]),
                "telefono": persona["telefono"],
                "cedula": persona["cedula"]
            }
    return None

@router.post("/consultar")
async def consultar_rostro(imagen: UploadFile = File(...), usuario_email: str = Depends(verificar_token)):
    try:
        file_path = guardar_imagen_temp(imagen)

        codificacion_facial = procesar_imagen(file_path)
        persona = obtener_persona_por_codificacion(codificacion_facial)

        if persona:
            return {
                "mensaje": "✅ Persona encontrada",
                "nombre": persona["nombre"],
                "apellido": persona["apellido"],
                "direccion": persona["direccion"],
                "fecha_nacimiento": persona["fecha_nacimiento"],
                "telefono": persona["telefono"],
                "cedula": persona["cedula"]
            }
        else:
            return {
                "mensaje": "❌ Persona NO encontrada"
            }
    except Exception:
        return {
            "mensaje": "❌ No se Detecto Rostro en la imagen"
        }
