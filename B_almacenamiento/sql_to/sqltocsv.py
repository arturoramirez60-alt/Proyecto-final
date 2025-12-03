from mysql.connector import connect, Error
from enum import Enum
from sqlalchemy import create_engine
import pandas as pd


"""
Este es un codigo aparte del programa, pero fue muy util para automatizar la extraccion de los csv's de las tablas de la base de datos en cada modificacion
"""
class DataDB(Enum):
    USER = "root"
    PASSWORD = "12345678"
    NAME_BD = "recursos_en_salud"
    SERVER = "127.0.0.1"
    

def conectar_mysql():
    try:
        sql_conexion = connect(
            host= DataDB.SERVER.value,
            user= DataDB.USER.value,
            password= DataDB.PASSWORD.value,
            database= DataDB.NAME_BD.value
        )
        return sql_conexion
    except Error as e:
        print(e)
        
def crear_conexion():
    cadena_conexion  = (f"mysql+mysqlconnector://"
                       f"{DataDB.USER.value}:"
                       f"{DataDB.PASSWORD.value}"
                       f"@{DataDB.SERVER.value}"
                       f"/{DataDB.NAME_BD.value}")

    return create_engine(cadena_conexion).connect()
"""
realiza un show tables para ver todas las tablas en la base de datos,
luego por cada tabla la convierte en un csv
- no recibe parametros
- no retorna nada
"""
def sqltocsv():
    conexion = conectar_mysql()
    cursor = conexion.cursor()
    cursor.execute("SHOW TABLES")
    tablas = cursor.fetchall() 
    for tabla in tablas:
        cadena_sql = crear_conexion()
        df = pd.read_sql(f"SELECT * FROM {tabla[0]}", cadena_sql)
        try:
            df.set_index("ID", inplace=True)
        except:
            df.set_index("Año", inplace=True)
        df.to_csv(f"B_almacenamiento/datasets/{tabla[0]}.csv")
    cursor.close() 
    conexion.close()
    
if __name__ == "__main__":
    sqltocsv()
        
        