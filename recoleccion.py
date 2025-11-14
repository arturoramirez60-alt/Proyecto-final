from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import time 
import pandas as pd


def abrir_navegador():
    
    s = Service(ChromeDriverManager().install())
    opc = Options()
    opc.add_argument("--start-maximized")
    navegador = webdriver.Chrome(service= s,options= opc)
    return navegador

def contenido(content):
    soup = bs(content, "html.parser")
    return soup

def derechohabiancia():
    
    poblacion_derechohabiencia = {"indicador" : [],
                                  "Porcentaje": [],
                                  "Año":[]}
    
    poblacion_afiliada = {"Estado":[],
                          "Porcentaje":[],
                          "Año":[]}
    
    
    navegador = abrir_navegador()
    navegador.get("https://www.inegi.org.mx/temas/derechohabiencia/")
    navegador.execute_script("document.body.style.zoom='10%'")
    
    wait = WebDriverWait(navegador, 5)
    boton_tabla = wait.until(EC.element_to_be_clickable((By.ID, "btn_tablagraf_gral0")))
    wait = WebDriverWait(navegador, 5)
    boton_tabla2 = wait.until(EC.element_to_be_clickable((By.ID, "btn_tablacont00")))
    
    boton_tabla.click()
    boton_tabla2.click()
    
    time.sleep(3)
    html = contenido(navegador.page_source)
    tablas = html.find_all("div", attrs= {"class":"card-body"})
    
    tabla1 = tablas[1]
    indicadores = tabla1.find_all("td", attrs= {"class":"TdInicio"})
    for indicador in indicadores:
        poblacion_derechohabiencia["indicador"].append(indicador.text)    
    porcentajes = tabla1.find_all("td", attrs= {"class":"Td"})
    for porcentaje in porcentajes:
        poblacion_derechohabiencia["Porcentaje"].append(porcentaje.text)
        poblacion_derechohabiencia["Año"].append(2020)
            
    tabla2 = tablas[2] 
    entidades = tabla2.find_all("td", attrs= {"class":"TdInicio notranslate"})
    for entidad in entidades:
        poblacion_afiliada["Estado"].append(entidad.text)
    porcentajes = tabla2.find_all("td", attrs= {"class":"Td"})
    for porcentaje in porcentajes:
        poblacion_afiliada["Porcentaje"].append(porcentaje.text)
        poblacion_afiliada["Año"].append(2020)
    
    navegador.close()
    
    df = pd.DataFrame(poblacion_derechohabiencia)
    df2 = pd.DataFrame(poblacion_afiliada)
    
    return df, df2

def navegar(navegador:webdriver.Chrome):
    
    time.sleep(3)
    navegador.execute_script("location.reload();")
    
    time.sleep(3)
    wait = WebDriverWait(navegador, 5)
    elemento = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='text-white' and contains(., 'Recursos en salud')]")))
    elemento.click()
    
    wait = WebDriverWait(navegador, 5)
    personal = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='list-group-item btn_desktop mb-0 pl-4 p-1 truncado' and contains(., 'Personal de salud')]")))
    personal.click()   
    time.sleep(3) 
    try:
        alerta = navegador.switch_to.alert
        print(f"Alerta después del segundo click: {alerta.text}")
        alerta.accept()
        time.sleep(3)
    except NoAlertPresentException:
        pass
     
def medicos_por_año():
    columnas_df = [ "Año",
           "Medicos generales, especialistas y odontologos",
           "Personal medico en formacion",
           "Medicos en otras labores",
           "Enfermeras generales y especialistas",
           "Pasantes de enfermeria",
           "Auxiliares de enfermeria",
           "Personal de enfermeria en otras labores",
           "Personal profesional",
           "Personal tecnico",
           "Otro personal",
           "TOTAL",
           "Estado"]
    filas_df = []
    
    navegador = abrir_navegador()
    navegador.get("http://sinaiscap.salud.gob.mx:8080/DGIS/")
    
    navegar(navegador)
    
    time.sleep(2)
    wait = WebDriverWait(navegador, 5)
    tabla = wait.until(EC.element_to_be_clickable((By.ID, "tabla20-tab")))
    tabla.click()
    wait = WebDriverWait(navegador, 5)
    elemento = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "filter-option-inner-inner")))
    elemento.click()
    time.sleep(2)
    
    html = contenido(navegador.page_source)
    estados = html.find_all("option")
    estados = [i.text for i in estados]
    estados = estados[0:33]
    
    for estado in estados:
        navegador.execute_script("document.body.style.zoom='50%'")
        
        wait = WebDriverWait(navegador, 5)
        i = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='{estado}']")))
        i.click()
        
        time.sleep(3)
        elemento.click()
        
        html = contenido(navegador.page_source)
        tabla = html.find("table",attrs={"class":"table table-sm table-bordered table-hover"})
        filas = tabla.find_all("tr")
        
        
        for fila in filas[1:]:
            columnas = fila.find_all("td")
            fila_temp = []
            
            for columna in columnas:
                fila_temp.append(columna.text)
            fila_temp.append(estado)
            filas_df.append(fila_temp)
            
    navegador.close()
    
    df = pd.DataFrame(filas_df, columns= columnas_df)
    return df

def medicos_por_institucion():
    
    data = {"institucion":[],
            "total":[]}
    navegador = abrir_navegador()
    navegador.get("http://sinaiscap.salud.gob.mx:8080/DGIS/")
    
    time.sleep(3) 
    navegar(navegador)  
    
    instituciones =  navegador.find_element(By.ID, "nav-Institucion-tab")
    instituciones.click()
    navegador.execute_script("document.body.style.zoom='50%'")
    time.sleep(3)
    tabla = navegador.find_element(By.ID, "tabla22-tab")
    tabla.click()
    boton = navegador.find_element(By.CSS_SELECTOR, "button[data-id='personalDeSalud_InstitucionAnio_anio']")
    boton.click()
    opcion_2020 = navegador.find_element(By.XPATH, "//span[contains(text(), '2020')]")
    opcion_2020.click()
    time.sleep(3)
    html = contenido(navegador.page_source)
    tabla = html.find_all("table", attrs={"class":"table table-sm table-bordered table-hover"})
    filas = tabla[2].find_all("tr")
    time.sleep(3)
    for fila in filas[1:]:
        
        columnas = fila.find_all("td")
        data["institucion"].append(columnas[0].text)
        data["total"].append(columnas[11].text)
        
    navegador.close()
    df =  pd.DataFrame(data)
    return df

def poblacion():

    data =  {"Año":[],
             "Poblacion":[]}
    
    navegador = abrir_navegador()
    navegador.get("https://www.inegi.org.mx/temas/estructura/")
    navegador.execute_script("document.body.style.zoom='10%'") 
    time.sleep(5)
    boton_tabla = navegador.find_element(By.ID, value= "btn_tablagraf_gral0")
    boton_tabla.click()
    time.sleep(5)
    html = contenido(navegador.page_source)

    tabla = html.find("div", attrs= {"class":"card-body"})

    años = tabla.find_all("td",attrs={"class":"TdInicioV"})
    for año in años:
        data["Año"].append(año.text)
    poblacion = tabla.find_all("td",attrs={"class":"TdV"})
    for personas in poblacion:
        data["Poblacion"].append(personas.text)
    
    navegador.close()
    
    df = pd.DataFrame(data)
    return df



    
    
    