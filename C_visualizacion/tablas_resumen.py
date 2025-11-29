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
        
    def Poblacion_afiliada(self):
        
        pa_pie = self.poblacion_afiliada
        pa_pie["Porcentaje_no_afiliado"] = 1 - pa_pie.Porcentaje_afiliado
        pa_pie["Porcentaje_total"] = 1 
        self.pa_pie = pd.melt(pa_pie, id_vars = ["Estado"], 
                value_vars = ["Porcentaje_afiliado","Porcentaje_no_afiliado"], 
                var_name= "porcentajes",
                value_name= "cantidad")
        
    def Personal_salud_año(self):
        psa_resumido =  self.personal_salud_año[["Año","Estado","TOTAL","Poblacion_total"]]
        
        
        self.psa_bar =  pd.melt(psa_resumido, id_vars= ["Año","Estado"], 
                                value_vars= ["TOTAL","Poblacion_total"],
                                var_name= "Poblacion",
                                value_name= "Total")
        
        self.psa_bar.Poblacion[self.psa_bar.Poblacion == "TOTAL"] = "Personal_medico"
        
    def Poblacion_derechohabiente(self):
        
        pd_bar =  self.poblacion_derechohabiente
        pd_bar["Poblacion_afiliada"] = pd_bar.Poblacion_total * pd_bar.Porcentaje_afiliado
        pd_bar.Poblacion_afiliada = round(pd_bar.Poblacion_afiliada,0)
        self.pd_bar = pd_bar[["institucion","Poblacion_afiliada"]]