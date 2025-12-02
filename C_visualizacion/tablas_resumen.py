import pandas as pd
from sqlalchemy import create_engine
from B_almacenamiento.database import conectar_mysql, DataDB, read_json
import pandas as pd
import json


class TablasResumen:
    def __init__(self):
        ps,user = read_json()
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
        renombre = {
            'TOTAL': 'Personal_medico'}
        psa_resumido.rename(columns=renombre, inplace=True)
        
        
        psa_bar =  pd.melt(psa_resumido, id_vars= ["Año","Estado"], 
                                value_vars= ["Personal_medico","Poblacion_total"],
                                var_name= "Poblacion",
                                value_name= "Total")
        self.psa_bar =  psa_bar
        
        psa_treemap =  self.personal_salud_año.drop(columns= "TOTAL")
        columnas = psa_treemap.columns[2:12]
        self.psa_treemap =  pd.melt(psa_treemap, id_vars=["Año","Estado"],
                                    value_vars= columnas,
                                    var_name= "Tipo_personal",
                                    value_name= "Total")
        
        
        self.psa_area =  psa_resumido[psa_resumido.Estado == "Nacional"] 
        
        self.psa_scatter = self.personal_salud_año[self.personal_salud_año.Estado != "Nacional"]
       
        psa_histogram =  self.personal_salud_año
        psa_histogram.drop(columns= "Poblacion_total", inplace= True)
        psa_histogram = psa_histogram[psa_histogram.Estado != 'Nacional']
        
        columnas =  psa_histogram.columns.to_list()[2:13]
        self.psa_histogram =  pd.melt(psa_histogram, id_vars= ["Año", "Estado"], value_vars= columnas, var_name= "Tipo_personal", value_name= "Total" )
        self.psa_histogram.Tipo_personal = self.psa_histogram.Tipo_personal.str.replace("TOTAL","Personal_total")
        
        
    def Poblacion_derechohabiente(self):
        
        pd_bar =  self.poblacion_derechohabiente
        pd_bar["Poblacion_afiliada"] = pd_bar.Poblacion_total * pd_bar.Porcentaje_afiliado
        pd_bar.Poblacion_afiliada = round(pd_bar.Poblacion_afiliada,0)
        
        self.pd_bar = pd_bar[["Institucion","Poblacion_afiliada","Porcentaje_afiliado"]]
    
    def Personal_salud_institucion(self):
        
        self.psi_treemap =  self.personal_salud_institucion[["Año","Institucion","Personal_total"]]
        
        psi_scatter =  self.personal_salud_institucion[["Institucion","Personal_total"]][self.personal_salud_institucion.Año == 2020]
   
        pd_scatter =  self.poblacion_derechohabiente
        pd_scatter["Poblacion_afiliada"] = pd_scatter.Poblacion_total * pd_scatter.Porcentaje_afiliado
        pd_scatter =  self.poblacion_derechohabiente[["Institucion","Poblacion_afiliada"]]
        
        self.psi_pd_scatter = pd.merge(psi_scatter,pd_scatter, how= "inner", on="Institucion")
        
        