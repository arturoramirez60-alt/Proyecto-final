import pandas as pd
from sqlalchemy import create_engine
from bases_de_datos import conectar_mysql
from bases_de_datos import DataDB

def cargar_dfs():
    ps = input("Ingrese la contraseña de su servidor mysql: ") 
    conexion = conectar_mysql(ps)
    cursor = conexion.cursor(dictionary=True)
    
    cursor.callproc("sp_poblacion_derechohabiente")
    for result in cursor.stored_results():
        poblacion_derechohabiente = pd.DataFrame(result.fetchall())
    
    cursor.callproc("sp_poblacion_afiliada")
    for result in cursor.stored_results():
        poblacion_afiliada = pd.DataFrame(result.fetchall())
        
    cursor.callproc("sp_personal_salud_año")
    for result in cursor.stored_results():
        personal_salud_año = pd.DataFrame(result.fetchall())
    
    cursor.callproc("sp_personal_salud_institucion")
    for result in cursor.stored_results():
        personal_salud_institucion = pd.DataFrame(result.fetchall())
    
    cursor.close()
    conexion.close()
    return poblacion_derechohabiente.set_index("ID"),poblacion_afiliada.set_index("ID"),personal_salud_año.set_index("ID"),personal_salud_institucion.set_index("ID")

def  crear_tablas_resumen():
    poblacion_derechohabiente,poblacion_afiliada,personal_salud_año,personal_salud_institucion = cargar_dfs()
    print(poblacion_derechohabiente.head())
    print(poblacion_afiliada.head())    
    print(personal_salud_año.head())
    print(personal_salud_institucion.head())
    
if __name__ == "__main__":
    crear_tablas_resumen()
    