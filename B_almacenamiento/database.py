from A_extraccion import limpieza as li
from sqlalchemy import create_engine
from sqlalchemy.types import INT, VARCHAR, DOUBLE
import pandas as pd
from enum import Enum
import pandas as  pd
from mysql.connector import connect, Error
import json

"""
Clase con los datos comunes que todo usuario debe tener para ejecutar el programa
"""
class DataDB(Enum):
    NAME_BD = "recursos_en_salud"
    SERVER = "127.0.0.1"
  
"""
Crea la cadena de conexion necesaria para conectar a pandas con MySQL
- recibe ps : contraseña, user : usuario 
- retorna la cadena de conexion
"""  
def crear_conexion(ps,user):
    cadena_conexion  = (f"mysql+mysqlconnector://"
                       f"{user}:"
                       f"{ps}"
                       f"@{DataDB.SERVER.value}"
                       f"/{DataDB.NAME_BD.value}")

    return create_engine(cadena_conexion).connect()

"""
Crea la conexion con MySQL
- recibe ps : contraseña, user : usuario
- retorna la conexion a MySQL
"""
def conectar_mysql(ps,user):

    conexion = connect(
            host= DataDB.SERVER.value,
            user= user,
            password= ps,
            database= DataDB.NAME_BD.value)
    return conexion
   
"""
Lee el archivo JSON para extraer la contraseña y el usuario
Esto se hace para que, una vez el usuario haya ejecutado el programa, pueda navegar libremente sin que requiera meter los mismos 
datos las veces que el programa lo necesite, al finalizar el programa se borra el JSON y el archivo solo se crea si la conexion fue exitosa
- No recibe parametros
- retorna ps : contraseña, user : usuario
""" 
def read_json():
    with open("_Archivos/conexion.json", "r") as archivo:
        datos = dict(json.loads(archivo.read()))
    user = datos["user"]
    ps = datos["password"]
    return ps,user
     
"""
Crea las llaves primarias de todas las tablas de la base de datos, esto se puede hacer asi ya que todas las tablas tienen la columna 'ID',
menos poblacion, cuya llave primaria el la columna 'Año' pero esta se intercepta en el try
- recibe ps : contraseña, user : usuario
- No retorna nada
""" 
def crear_llaves_primarias(ps,user):
    
    conexion = conectar_mysql(ps,user)
    cursor = conexion.cursor()
    cursor.execute("show tables")
    tablas = cursor.fetchall()
    for tabla in tablas:
        try:
            #Para todas las tablas cuya llave primaria es ID 
            cursor.execute(f"ALTER TABLE `recursos_en_salud`.`{tabla[0]}` CHANGE COLUMN `ID` `ID` INT NOT NULL ,ADD PRIMARY KEY (`ID`);;")
        except:
            #Como solo en poblacion total la llave primaria no es ID entonces funcionara
            cursor.execute("ALTER TABLE `recursos_en_salud`.`poblacion_total` CHANGE COLUMN `Año` `Año` INT NOT NULL ,ADD PRIMARY KEY (`Año`);;")
    conexion.commit()
    cursor.close()
    cursor.close()
    
"""
Crea las relaciones de llave primaria a llave foranea segun el modelo de la base de datos relacional
- recibe ps : contraseña, user : usuario
- No retorna nada
"""
def crear_relaciones(ps,user):
    conexion = conectar_mysql(ps,user)
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
    #relacion con tabla poblacion_total FK
    cursor.execute("ALTER TABLE recursos_en_salud.personal_salud_institucion ADD CONSTRAINT fk_personal_instituciones_año FOREIGN KEY (Año) REFERENCES recursos_en_salud.poblacion_total(Año);") 
    conexion.commit()
    cursor.close()
    conexion.close()

"""
Crea los store procedures de la base de datos, los cuales ayudaran a llamar las tablas sin los ID's de referencia, en lugar de eso, el nombre del dato corespondiente
- recibe ps : contraseña, user : usuario
- No retorna nada
"""
def crear_procedures(ps,user):
    conexion = conectar_mysql(ps,user)
    cursor = conexion.cursor()
    
    #procedure para personal_salud_año
    cursor.execute( "create procedure sp_personal_salud_año() begin"
	                " select psa.*, e.Estado, pt.Poblacion as Poblacion_total"
	                " from personal_salud_año as psa "
	                " left join estados as e on e.ID = psa.ID_Estado"
	                " left join poblacion_total as pt on psa.Año = pt.Año;"
                    " end")

    #procedure para personal_salud_institucion
    cursor.execute( "create procedure sp_personal_salud_institucion() begin"
	                " select psi.ID, pa.Año, i.Institucion, psi.total as Personal_total,pa.poblacion as poblacion_total from  personal_salud_institucion as psi"
	                " left join instituciones as i on i.ID = psi.ID_institucion"
                    " left join poblacion_total as pa on pa.Año = psi.Año; end")

    #procedure para poblacion_afiliada
    cursor.execute( "create procedure sp_poblacion_afiliada() begin"
                    " select pa.ID, e.Estado, pa.Porcentaje as Porcentaje_afiliado from poblacion_afiliada as pa"
                    " left join estados as e on e.ID = pa.ID_Estado; end")

    #procedures para poblacion_derechohabiente
    cursor.execute( "create procedure sp_poblacion_derechohabiente() begin"
                    " select pdh.ID,i.institucion as Institucion ,pdh.Año,pt.Poblacion as Poblacion_total,pdh.Porcentaje as Porcentaje_afiliado from poblacion_derechohabiente as pdh"
                    " left join instituciones as i on i.ID = pdh.ID_institucion"
                    " left join poblacion_total as pt on pdh.Año = pt.Año; end")

    #procedure para poblacion__total
    cursor.execute( "create procedure sp_poblacion_total() begin"
                    " select * from poblacion_total; end")

    
    conexion.commit()
    cursor.close()
    conexion.close()
    
"""
Crea las tablas en MySQL asignado tipo de dato a cada columna de cada tabla,
- recibe ps : contraseña, user : usuario y todas las tablas de la base de datos
- No retorna nada
"""

def crear_tablas_sql(ps,user,poblacion_afiliada,poblacion_derechohabiente,personal_salud_año,personal_salud_institucion,poblacion_total,estados,instituciones):
    
    conexion =  crear_conexion(ps,user)
    poblacion_derechohabiente.to_sql("poblacion_derechohabiente",conexion, if_exists =  "replace", dtype={"ID":INT,"ID_Institucion":INT,"Porcentaje":DOUBLE,"Año":INT})
    poblacion_afiliada.to_sql("poblacion_afiliada",conexion, if_exists =  "replace",dtype={"ID":INT,"ID_Estado":INT,"Porcentaje":DOUBLE,"Año":INT})
    personal_salud_año.to_sql("personal_salud_año",conexion,if_exists="replace",dtype={ "ID": INT,
                                                                                        "ID_Estado": INT,
                                                                                        "Año": INT,
                                                                                        "Medicos_generales_especialistas_y_odontologos": INT,
                                                                                        "Personal_medico_en_formacion": INT,
                                                                                        "Medicos_en_otras_labores": INT,
                                                                                        "Enfermeras_generales_y_especialistas": INT,
                                                                                        "Pasantes_de_enfermeria": INT,
                                                                                        "Auxiliares_de_enfermeria": INT,
                                                                                        "Personal_de_enfermeria_en_otras_labores": INT,
                                                                                        "Personal_profesional": INT,
                                                                                        "Personal_tecnico": INT,
                                                                                        "Otro_personal": INT,
                                                                                        "TOTAL": INT})
    
    personal_salud_institucion.to_sql("personal_salud_institucion",conexion, if_exists = "replace",dtype= {"ID":INT,"ID_Institucion":INT,"Año":INT,"total":INT})
    poblacion_total.to_sql("poblacion_total",conexion, if_exists =  "replace",dtype={"Año":INT,"Poblacion":INT})
    instituciones.to_sql("instituciones",conexion, if_exists =  "replace", dtype={"ID":INT,"Institucion":VARCHAR(50)})
    estados.to_sql("estados",conexion, if_exists =  "replace", dtype={"ID":INT,"Estado":VARCHAR(25)})
    conexion.close()
    
    
"""
ejecuta las funciones de limpieza, que a su vez ejecutan las funciones de extraccion, para posteriormente crear las tablas en mysql, llaves primarias, relaciones y procedures
estos 3 ultimos encerrados en en try por que no se pueden repetir los procedures ni las relaciones
- recibe ps : contraseña, user : usuario
- No retorna nada
"""
def crear_tablas_webscraper(ps,user):
    
    poblacion_derechohabiente = li.limpiar_poblacion_derechohabiente()
    poblacion_afiliada = li.limpiar_poblacion_afilada()
    personal_salud_año = li.limpiar_personal_salud_año()
    personal_salud_institucion =  li.limpiar_personal_salud_institucion()
    poblacion_total =  li.limpiar_poblacion()
    _,estados =  li.crear_estados()
    _,instituciones =  li.crear_instituciones()
    
    crear_tablas_sql(ps,user,poblacion_afiliada,poblacion_derechohabiente,personal_salud_año,personal_salud_institucion,poblacion_total,estados,instituciones)
    try:
        crear_llaves_primarias(ps,user)
        crear_relaciones(ps,user)
        crear_procedures(ps,user)
    except:
        pass
    print("se crearon las tablas en la base de datos")

"""
Por medio de archivos cvs, crea las tablas en la base de datos, estos archivos csv son porducto de utilizar el codigo 'csvtosql' el cual se encuentra en la 
carpeta 'sql_to', primero se creo la base de datos con el web scraping y despues se ejecuto ese archivo para obtener los csv's
crear las tablas en mysql, llaves primarias, relaciones y procedures
estos 3 ultimos encerrados en en try por que no se pueden repetir los procedures ni las relaciones
- recibe ps : contraseña, user : usuario
- No retorna nada
"""
def crear_tablas_csv(ps,user):
    ruta_relativa = "B_almacenamiento/datasets"
    poblacion_derechohabiente = pd.read_csv(f"{ruta_relativa}/poblacion_derechohabiente.csv",index_col="ID")
    poblacion_afiliada = pd.read_csv(f"{ruta_relativa}/poblacion_afiliada.csv",index_col="ID")
    personal_salud_año = pd.read_csv(f"{ruta_relativa}/personal_salud_año.csv",index_col="ID")
    personal_salud_institucion =  pd.read_csv(f"{ruta_relativa}/personal_salud_institucion.csv",index_col="ID")
    poblacion_total =  pd.read_csv(f"{ruta_relativa}/poblacion_total.csv",index_col="Año")
    estados =  pd.read_csv(f"{ruta_relativa}/estados.csv",index_col="ID")
    instituciones =  pd.read_csv(f"{ruta_relativa}/instituciones.csv",index_col="ID")

    crear_tablas_sql(ps,user,poblacion_afiliada,poblacion_derechohabiente,personal_salud_año,personal_salud_institucion,poblacion_total,estados,instituciones)
    try:
        crear_llaves_primarias(ps,user)
        crear_relaciones(ps,user)
        crear_procedures(ps,user)
    except:
        pass

    print("se crearon las tablas en la base de datos")
    




    

    
