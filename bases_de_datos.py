import limpieza as li
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR, INTEGER
import pandas as pd
from enum import Enum

import pandas as  pd

class DataDB(Enum):
    USER = "root"
    NAME_BD = "recursos_en_salud"
    SERVER = "127.0.0.1"
    
def crear_conexion(ps):
    cadena_conexion  = (f"mysql+mysqlconnector://"
                       f"{DataDB.USER.value}:"
                       f"{ps}"
                       f"@{DataDB.SERVER.value}"
                       f"/{DataDB.NAME_BD.value}")

    return create_engine(cadena_conexion).connect()

def crear_tablas_webscraper(ps):
    
    conexion =  crear_conexion(ps)
 
    poblacion_derechohabiente = li.limpiar_poblacion_derechohabiente()
    poblacion_derechohabiente.to_sql("poblacion_derechohabiente",conexion, if_exists =  "replace")
    
    poblacion_afiliada = li.limpiar_poblacion_afilada()
    poblacion_afiliada.to_sql("poblacion_afiliada",conexion, if_exists =  "replace")
    
    personal_salud_año = li.limpiar_personal_salud_año()
    personal_salud_año.to_sql("personal_salud_año",conexion, if_exists =  "replace")
    
    personal_salud_institucion =  li.limpiar_personal_salud_institucion()
    personal_salud_institucion.to_sql("personal_salud_institucion",conexion, if_exists =  "replace")
    
    poblacion_total =  li.limpiar_poblacion()
    poblacion_total.to_sql("poblacion_total",conexion, if_exists =  "replace")
    
    _,Estados =  li.crear_estados()
    Estados.to_sql("Estados",conexion, if_exists =  "replace")
    
    _,Instituciones =  li.crear_instituciones()
    Instituciones.to_sql("Instituciones",conexion, if_exists =  "replace")
    
def crear_tablas_csv():
    print("aqui debera haber algo, pero me dio weba")



    

    
