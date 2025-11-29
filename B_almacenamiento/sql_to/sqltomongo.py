from mysql.connector import connect
from pymongo import MongoClient
import datetime

def conectar(db):
    return connect(host="localhost",
                           user="root", 
                           password="12345678", 
                           database= db)
     
def conectar_mongodb(db):
    cliente = MongoClient("mongodb://localhost:27017/")
    mongo_conexion = cliente[db]
    return mongo_conexion

def limpiar_documento(documento):
    for clave, valor in documento.items():
        if isinstance(valor, datetime.date) and not isinstance(valor, datetime.datetime):
            documento[clave] = datetime.datetime.combine(valor, datetime.time.min)
    return documento
    
def migrar(db):
    sql_conexion = conectar(db)
    mongo_conexion = conectar_mongodb(db)
    
    cursor = sql_conexion.cursor(dictionary=True)
    cursor.execute("SHOW TABLES")
    tablas = cursor.fetchall()
    
    for tabla in tablas:
        tabla = list(tabla.values())[0]
        cursor.execute(f"SELECT * FROM {tabla}")
        documentos_sql = cursor.fetchall()
        documentos_mongo = [limpiar_documento(doc) for doc in documentos_sql]
        mongo_conexion[tabla].drop()
        mongo_conexion[tabla].insert_many(documentos_mongo)
         
        
    cursor.close()
    sql_conexion.close()
    mongo_conexion.client.close()
    
if __name__ == "__main__":
    migrar("recursos_en_salud")