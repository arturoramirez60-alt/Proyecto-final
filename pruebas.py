from A_extraccion import limpieza as li
from C_visualizacion import tablas_resumen as tr


if __name__ == "__main__":
  tablas = tr.TablasResumen()
  tablas.Poblacion_afiliada()
  tablas.Personal_salud_año()
  tablas.Poblacion_derechohabiente()
  
  pd_bar =  tablas.poblacion_derechohabiente
  
  print(pd_bar)
  