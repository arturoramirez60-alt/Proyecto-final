import limpieza as li
from sqlalchemy import create_engine
from sqlalchemy.types import INT
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
                       f"{DataDB.PASSWORD.value}"
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
        
def crear_llaves_primarias(ps):
    
    conexion = conectar_mysql(ps)
    cursor = conexion.cursor()
    cursor.execute("show tables")
    tablas = cursor.fetchall()
    for tabla in tablas:
        try:
            #Para todas las tablas cuya llave primaria es ID 
            cursor.execute(f"ALTER TABLE `recursos_en_salud`.`{tabla[0]}` CHANGE COLUMN `ID` `ID` INT NOT NULL ,ADD PRIMARY KEY (`ID`);;")
        except:
            cursor.execute("ALTER TABLE `recursos_en_salud`.`poblacion_total` CHANGE COLUMN `Año` `Año` INT NOT NULL ,ADD PRIMARY KEY (`Año`);;")
    conexion.commit()
    cursor.close()
    cursor.close()
    
def crear_relaciones(ps):
    conexion = conectar_mysql(ps)
    cursor = conexion.cursor()
    #Relacion con tabla poblacion_total FK
    cursor.execute("ALTER TABLE recursos_en_salud.personal_salud_año ADD CONSTRAINT fk_personal_año FOREIGN KEY (Año) REFERENCES recursos_en_salud.poblacion_total(Año);")
    #Relacion con tabla estados FKRelacion con tabla estados FK
    cursor.execute("ALTER TABLE recursos_en_salud.personal_salud_año ADD CONSTRAINT fk_personal_estado FOREIGN KEY (ID_Estado) REFERENCES recursos_en_salud.estados(ID);")
    #Relacion con tabla poblacion_total FK
    cursor.execute("ALTER TABLE recursos_en_salud.poblacion_afiliada ADD CONSTRAINT fk_afiliados_año FOREIGN KEY (Año) REFERENCES recursos_en_salud.poblacion_total(Año);")
    #Relacion con tabla estado FK
    cursor.execute("ALTER TABLE recursos_en_salud.poblacion_afiliada ADD CONSTRAINT fk_poblacion_estado FOREIGN KEY (ID_Estado) REFERENCES recursos_en_salud.estados(ID);")
    #Relacion con tabla poblacion_total FK
    cursor.execute("ALTER TABLE recursos_en_salud.poblacion_derechohabiente ADD CONSTRAINT fk_derechohabientes_año FOREIGN KEY (Año) REFERENCES recursos_en_salud.poblacion_total(Año);")
    #Relacion con tabla instituciones FK
    cursor.execute("ALTER TABLE recursos_en_salud.poblacion_derechohabiente ADD CONSTRAINT fk_institucion_derechohabientes FOREIGN KEY (ID_Institucion) REFERENCES recursos_en_salud.instituciones(ID);")
    #Relacion con tabla instituciones FK 
    cursor.execute("ALTER TABLE recursos_en_salud.personal_salud_institucion ADD CONSTRAINT fk_personal_instituciones FOREIGN KEY (ID_Institucion) REFERENCES recursos_en_salud.instituciones(ID);") 
    conexion.commit()
    cursor.close()
    conexion.close()

def crear_tablas_webscraper(ps):
    
 
    conexion =  crear_conexion(ps)
    print(conexion)
        
    print("El programa se esta ejecutando, espere por favor")
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
    
    crear_llaves_primarias(ps)
    crear_relaciones(ps)
    
    print("ya quedo")
    
def crear_tablas_csv(ps):
    conexion =  crear_conexion(ps)
 
    poblacion_derechohabiente = pd.read_csv("datasets/poblacion_derechohabiente.csv",index_col="ID")
    poblacion_derechohabiente.to_sql("poblacion_derechohabiente",conexion, if_exists =  "replace", dtype={"ID":INT,"ID_Institucion":INT,"Año":INT})
    
    poblacion_afiliada = pd.read_csv("datasets/poblacion_afiliada.csv",index_col="ID")
    poblacion_afiliada.to_sql("poblacion_afiliada",conexion, if_exists =  "replace",dtype={"ID":INT,"ID_Estado":INT,"Año":INT})
    
    personal_salud_año = pd.read_csv("datasets/personal_salud_año.csv",index_col="ID")
    personal_salud_año.to_sql("personal_salud_año",conexion, if_exists =  "replace",dtype={"ID":INT,"ID_Estado":INT,"Año":INT})
    
    personal_salud_institucion =  pd.read_csv("datasets/personal_salud_institucion.csv",index_col="ID")
    personal_salud_institucion.to_sql("personal_salud_institucion",conexion, if_exists =  "replace",dtype={"ID":INT,"ID_Institucion":INT})
    
    poblacion_total =  pd.read_csv("datasets/poblacion_total.csv",index_col="Año")
    poblacion_total.to_sql("poblacion_total",conexion, if_exists =  "replace",dtype={"Año":INT})
    
    estados =  pd.read_csv("datasets/estados.csv",index_col="ID")
    estados.to_sql("estados",conexion, if_exists =  "replace", dtype={"ID":INT})
    
    instituciones =  pd.read_csv("datasets/instituciones.csv",index_col="ID")
    instituciones.to_sql("instituciones",conexion, if_exists =  "replace", dtype={"ID":INT})
    
    crear_llaves_primarias(ps)
    crear_relaciones(ps)
    
    print("ya quedo")
    




    

    
