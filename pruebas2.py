import json
import os


with open("_Archivos/conexion.json", "r") as archivo:
    datos = dict(json.loads(archivo.read()))

user = datos["user"]
ps = datos["password"]
    
print(user,ps)