from mysql.connector import connect, Error
from pymongo import MongoClient
from bases_de_datos import DataDB
from bases_de_datos import conectar_mysql

     
def conectar_mongodb():
    cliente = MongoClient("mongodb://localhost:27017/")
    mongo_conexion = cliente[f"{DataDB.NAME_BD.value}"]
    return mongo_conexion

def migrar(ps):
    sql_conexion = conectar_mysql(ps)
    mongo_conexion = conectar_mongodb()
    
    cursor = sql_conexion.cursor()
    cursor.execute("SHOW TABLES")
    tablas = cursor.fetchall()
    
    for tabla in tablas:
        cursor2 =  sql_conexion.cursor(dictionary=True)
        cursor2.execute(f"SELECT * FROM {tabla[0]}")
        documentos = cursor2.fetchall()
        mongo_conexion[tabla[0]].insert_many(documentos)
 
    cursor.close()
    sql_conexion.close()
    mongo_conexion.client.close()
    
if __name__ == "__main__":
    password = input("Ingrese la contraseña de MySQL: ")
    migrar(password)