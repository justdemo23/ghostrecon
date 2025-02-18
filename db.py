import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # ⚠️ Reemplaza con tu usuario de MySQL
        password="A25bd1e23",  # ⚠️ Reemplaza con tu contraseña de MySQL
        database="reconocimiento_facial"  # ⚠️ Reemplaza con el nombre de tu BD
    )

def get_db_cursor():
    return get_db_connection().cursor()

def close_db_connection(cursor, conn):
    cursor.close()
    conn.close()