import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="worlddb.cjwu6cgm66rf.us-east-2.rds.amazonaws.com",
        user="admin",
        password="miprimerapp",
        database="world",
        port=3306,
    )

def obtener_paises():
    conn = connect_db()
    if conn.is_connected():
        print("Conexión exitosa a la base de datos")
    else:
        print("Error al conectar a la base de datos")
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM world.country")
    paises = cursor.fetchall()
    cursor.close()
    conn.close()
    return paises

def obtener_ciudades():
    conn = connect_db()
    if conn.is_connected():
        print("Conexión exitosa a la base de datos")
    else:
        print("Error al conectar a la base de datos")
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT ID, Name, CountryCode, District, Population FROM city")
    ciudades = cursor.fetchall()
    cursor.close()
    conn.close()
    return ciudades