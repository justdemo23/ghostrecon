import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tu_contraseña",
        database="reconocimiento_facial"
    )

def get_db_cursor():
    return get_db_connection().cursor()

def close_db_connection(cursor, conn):
    cursor.close()
    conn.close()