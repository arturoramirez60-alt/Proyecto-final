import limpieza as li
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR, INTEGER
import pandas as pd
from enum import Enum
import pandas as  pd
from mysql.connector import connect, Error



class DataDB(Enum):
    USER = "root"
    PASSWORD = "12345678"
    NAME_BD = "recursos_en_salud"
    SERVER = "127.0.0.1"
    
def crear_conexion(ps):
    cadena_conexion  = (f"mysql+mysqlconnector://"
                       f"{DataDB.USER.value}:"
                       f"{ps}"
                       f"@{DataDB.SERVER.value}"
                       f"/{DataDB.NAME_BD.value}")

    return create_engine(cadena_conexion).connect()

def conectar_mysql(ps):
    try:
        conexion = connect(
            host= DataDB.SERVER.value,
            user= DataDB.USER.value,
            password= ps,
            database= DataDB.NAME_BD.value
        )
        return conexion
    except Error as e:
        print(e)
        
def crear_llaves_foraneas(ps):
    pass

def crear_llaves_primaras(ps):
    conexion = conectar_mysql(ps)
    cursor = conexion.cursor()
    

    #para estados
    cursor.execute("ALTER TABLE `recursos_en_salud`.`estados` CHANGE COLUMN `ID` `ID` BIGINT NOT NULL ,ADD PRIMARY KEY (`ID`);;")
    #para instituciones
    cursor.execute("ALTER TABLE `recursos_en_salud`.`instituciones` CHANGE COLUMN `ID` `ID` BIGINT NOT NULL ,ADD PRIMARY KEY (`ID`);;")
    #para personal salud año
    cursor.execute("ALTER TABLE `recursos_en_salud`.`personal_salud_año` CHANGE COLUMN `ID` `ID` BIGINT NOT NULL ,ADD PRIMARY KEY (`ID`);;")
    #para poblacion derechohabiente
    cursor.execute("ALTER TABLE `recursos_en_salud`.`poblacion_derechohabiente` CHANGE COLUMN `ID` `ID` BIGINT NOT NULL ,ADD PRIMARY KEY (`ID`);;")
    #para poblacion afiliada
    cursor.execute("ALTER TABLE `recursos_en_salud`.`poblacion_afiliada` CHANGE COLUMN `ID` `ID` BIGINT NOT NULL ,ADD PRIMARY KEY (`ID`);;")
    #para personal salud institucion
    cursor.execute("ALTER TABLE `recursos_en_salud`.`personal_salud_institucion` CHANGE COLUMN `ID` `ID` BIGINT NOT NULL ,ADD PRIMARY KEY (`ID`);;")
    #para poblacion total
    cursor.execute("ALTER TABLE `recursos_en_salud`.`poblacion_total` CHANGE COLUMN `Año` `Año` BIGINT NOT NULL ,ADD PRIMARY KEY (`Año`);;")
    
    conexion.commit()
    cursor.close()
    conexion.close()
    
def crear_tablas_webscraper(ps):
    print("El programa se esta ejecutando, espere por favor")
    Estado = True
    while Estado:
        try:
            conexion =  crear_conexion(ps)
            Estado = False
        except:
            ps = input("contraseña incorrecta, intente de nuevo: ")
        
 
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
    print(poblacion_total)
    
    _,estados =  li.crear_estados()
    estados.to_sql("estados",conexion, if_exists =  "replace")
    
    _,instituciones =  li.crear_instituciones()
    instituciones.to_sql("instituciones",conexion, if_exists =  "replace")
    
    crear_llaves_primaras(ps)
    
    print("ya quedo")
    
def crear_tablas_csv(ps):
    conexion =  crear_conexion(ps)
 
    poblacion_derechohabiente = pd.read_csv("datasets/poblacion_derechohabiente.csv",index_col="ID")
    poblacion_derechohabiente.to_sql("poblacion_derechohabiente",conexion, if_exists =  "replace")
    
    poblacion_afiliada = pd.read_csv("datasets/poblacion_afiliada.csv",index_col="ID")
    poblacion_afiliada.to_sql("poblacion_afiliada",conexion, if_exists =  "replace")
    
    personal_salud_año = pd.read_csv("datasets/personal_salud_año.csv",index_col="ID")
    personal_salud_año.to_sql("personal_salud_año",conexion, if_exists =  "replace")
    
    personal_salud_institucion =  pd.read_csv("datasets/personal_salud_institucion.csv",index_col="ID")
    personal_salud_institucion.to_sql("personal_salud_institucion",conexion, if_exists =  "replace")
    
    poblacion_total =  pd.read_csv("datasets/poblacion_total.csv",index_col="Año")
    poblacion_total.to_sql("poblacion_total",conexion, if_exists =  "replace")
    
    estados =  pd.read_csv("datasets/estados.csv",index_col="ID")
    estados.to_sql("estados",conexion, if_exists =  "replace")
    
    instituciones =  pd.read_csv("datasets/instituciones.csv",index_col="ID")
    instituciones.to_sql("instituciones",conexion, if_exists =  "replace")
    
    crear_llaves_primaras(ps)
    
    print("ya quedo")
    




    

    
