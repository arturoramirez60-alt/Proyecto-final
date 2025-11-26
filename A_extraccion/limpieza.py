from  A_extraccion import recoleccion as rec
import pandas as pd
import pandas as  pd

def crear_instituciones():
    instituciones_diccionario = {
        "IMSS": 1,
        "IMSS_BIENESTAR": 2,
        "ISSSTE": 3,
        "INSABI_O_SEGURO_POPULAR": 4,
        "ISSSTE_O_ISSSTE_ESTATAL": 5,
        "INSTITUCION_PRIVADA": 6,
        "PEMEX_SDN_O_SM": 7,
        "OTRA_INSTITUCION": 8,
        "DIF": 9,
        "ESTATALES": 10,
        "MUNICIPAL": 11,
        "PEMEX": 12,
        "SALUD": 13,
        "SEDENA": 14,
        "SEMAR": 15,
        "UNIVERSITARIO": 16,
        "CENTROS_DE_INTEGRACION_JUVENIL":17}
    
    instituciones = {
    "ID": [i for i in range(1,18)],
    "Institucion": [
        "IMSS",
        "IMSS_BIENESTAR",
        "ISSSTE",
        "INSABI_O_SEGURO_POPULAR",
        "ISSSTE_O_ISSSTE_ESTATAL",
        "INSTITUCION_PRIVADA",
        "PEMEX_SDN_O_SM",
        "OTRA_INSTITUCION",
        "DIF",
        "ESTATALES",
        "MUNICIPAL",
        "PEMEX",
        "SALUD",
        "SEDENA",
        "SEMAR",
        "UNIVERSITARIO",
        "CENTROS_DE_INTEGRACION_JUVENIL"
    ]}

    df_instituciones =  pd.DataFrame(instituciones)
    crear_indice(df_instituciones)
    return instituciones_diccionario,df_instituciones

def crear_estados():
    estados = {
    "ID": [i for i in range(1,34)],
    "Estado": [
        "Aguascalientes",
        "Baja_California",
        "Baja_California_Sur",
        "Campeche",
        "Chiapas",
        "Chihuahua",
        "Coahuila",
        "Colima",
        "Ciudad_de_México",
        "Durango",
        "Guanajuato",
        "Guerrero",
        "Hidalgo",
        "Jalisco",
        "México",
        "Michoacán",
        "Morelos",
        "Nayarit",
        "Nuevo_León",
        "Oaxaca",
        "Puebla",
        "Querétaro",
        "Quintana_Roo",
        "San_Luis_Potosí",
        "Sinaloa",
        "Sonora",
        "Tabasco",
        "Tamaulipas",
        "Tlaxcala",
        "Veracruz",
        "Yucatán",
        "Zacatecas",
        "Nacional"
    ]}
    
    estados_diccionario = {
    "AGUASCALIENTES": 1,
    "BAJA_CALIFORNIA": 2,
    "BAJA_CALIFORNIA_SUR": 3,
    "CAMPECHE": 4,
    "CHIAPAS": 5,
    "CHIHUAHUA": 6,
    "COAHUILA": 7,
    "COLIMA": 8,
    "CIUDAD_DE_MÉXICO": 9,
    "DURANGO": 10,
    "GUANAJUATO": 11,
    "GUERRERO": 12,
    "HIDALGO": 13,
    "JALISCO": 14,
    "MÉXICO": 15,
    "MICHOACÁN": 16,
    "MORELOS": 17,
    "NAYARIT": 18,
    "NUEVO_LEÓN": 19,
    "OAXACA": 20,
    "PUEBLA": 21,
    "QUERÉTARO": 22,
    "QUINTANA_ROO": 23,
    "SAN_LUIS_POTOSÍ": 24,
    "SINALOA": 25,
    "SONORA": 26,
    "TABASCO": 27,
    "TAMAULIPAS": 28,
    "TLAXCALA": 29,
    "VERACRUZ": 30,
    "YUCATÁN": 31,
    "ZACATECAS": 32,
    "NACIONAL": 33 }
    
    df_estados =  pd.DataFrame(estados)
    crear_indice(df_estados)
    return estados_diccionario, df_estados

def limpiar_columnas(df:pd.DataFrame):
    
    cols =  df.columns
    for col in cols:
        df[col] = df[col].astype("str")
        df[col] = df[col].str.replace(",","")
        df[col] = df[col].str.replace("\n","")
    return df

def crear_indice(df:pd.DataFrame):
    
    indices =  [i + 1 for i in range(len(df))]
    df["ID"] = indices
    df.set_index("ID",inplace= True)
    return df
    
def mapear_instituciones(df:pd.DataFrame):
    
    instituciones,_ =  crear_instituciones()
    df.ID_Institucion =  df.ID_Institucion.map(instituciones)
    return df

def mapear_estados(df:pd.DataFrame):
    
    estados,_ = crear_estados()
    df.ID_Estado = df.ID_Estado.map(estados)
    return df

def limpiar_poblacion_derechohabiente():
    
    df, _ = rec.derechohabiancia() 
    limpiar_columnas(df)
    df["ID_Institucion"] = df.indicador
    df.ID_Institucion = df.ID_Institucion.str.upper()
    df.drop(columns= "indicador", inplace= True)
    mapear_instituciones(df)
    crear_indice(df)
    df = df[["ID_Institucion","Porcentaje","Año"]]
    return df

def limpiar_poblacion_afilada():

    _, df = rec.derechohabiancia() 
    limpiar_columnas(df)
    df["ID_Estado"] = df.Estado
    df.drop(columns="Estado",inplace=True)
    df.ID_Estado = df.ID_Estado.str.replace("Coahuila de Zaragoza","COAHUILA")
    df.ID_Estado = df.ID_Estado.str.replace("Estados Unidos Mexicanos","NACIONAL")
    df.ID_Estado = df.ID_Estado.str.replace("Veracruz de Ignacio de la Llave","VERACRUZ")
    df.ID_Estado = df.ID_Estado.str.replace("Michoacán de Ocampo","MICHOACÁN")
    df.ID_Estado = df.ID_Estado.str.upper()
    mapear_estados(df)
    crear_indice(df)
    df = df[["ID_Estado","Porcentaje","Año"]]
    return df
    
def limpiar_personal_salud_año():
    
    df = rec.personal_por_año()
    limpiar_columnas(df)
    df["ID_Estado"] = df.Estado
    df.drop(columns="Estado",inplace=True)
    mapear_estados(df)
    crear_indice(df)
    return df

def limpiar_personal_salud_institucion():
    
    df =  rec.personal_por_institucion()
    limpiar_columnas(df)
    df["ID_Institucion"] = df.institucion
    df.ID_Institucion = df.ID_Institucion.str.upper()
    df.drop(columns= "institucion", inplace= True)
    mapear_instituciones(df)
    crear_indice(df)
    df =  df[["ID_Institucion","total","Año"]]
    return df
    
def limpiar_poblacion():

    df_temp = rec.poblacion()
    df_temp.Año = df_temp.Año.astype("int")
    data = {"Año":[i for i in range(1910,2026)]}
    df =  pd.DataFrame(data)
    df = df.merge(df_temp, on="Año", how="left")
    df.ffill(inplace=True)
    df.set_index("Año",inplace= True)
    limpiar_columnas(df)
    return df
    
     
