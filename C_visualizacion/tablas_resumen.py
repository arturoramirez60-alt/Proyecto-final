import pandas as pd
from sqlalchemy import create_engine
from B_almacenamiento.database import conectar_mysql, DataDB
import pandas as pd

class TablasResumen:
    def __init__(self):
        ps = input("Ingrese la contraseña de su servidor mysql: ") 
        user = input("Ingrese su nombre de usuario de mysql: ")
        conexion = conectar_mysql(ps,user)
        cursor = conexion.cursor(dictionary=True)
        
        cursor.callproc("sp_poblacion_derechohabiente")
        for result in cursor.stored_results():
            self.poblacion_derechohabiente = pd.DataFrame(result.fetchall())
        
        cursor.callproc("sp_poblacion_afiliada")
        for result in cursor.stored_results():
            self.poblacion_afiliada = pd.DataFrame(result.fetchall())
            
        cursor.callproc("sp_personal_salud_año")
        for result in cursor.stored_results():
            self.personal_salud_año = pd.DataFrame(result.fetchall())
        
        cursor.callproc("sp_personal_salud_institucion")
        for result in cursor.stored_results():
            self.personal_salud_institucion = pd.DataFrame(result.fetchall())
        cursor.close()
        conexion.close()