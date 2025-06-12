import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root@localhost",
        password="root",
        database="world"
    )
