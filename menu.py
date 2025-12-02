from B_almacenamiento import database as db
from C_visualizacion import inicio
from mysql.connector import connect, Error
import json
import os

def conectar_basededatos():
    
    user = input("nombre de usuario: ")
    ps = input("contraseña de su servidor: ")
    try:
        db.conectar_mysql(ps,user)
        datos = {
                "user": user,
                "password": ps
                }
        try:
            os.remove('_Archivos/conexion.json')
        except:
            pass
        with open('_Archivos/conexion.json', "w") as archivo:
            archivo.write(json.dumps(datos))

        return True
    
    except Error as e:
        if e.errno == 1049:
            print("-------------------------------------------------------")
            print("Cree la base de datos 'recursos_en_salud' en MySQL")
            print("-------------------------------------------------------")
        if e.errno == 1045:
            print("-------------------------------------------------------")
            print("Usuario o contraseña incorrectos")
            print("-------------------------------------------------------")

        return False

def main():
    
    
    opc =  0
    while opc != 4:
        ps,user = db.read_json()
        opc = int(input("1. Crear tablas con webscrapper\n2. Crear tablas desde csv\n3. Dashboard\n4. salir\n"))
        if opc == 1:
            db.crear_tablas_webscraper(ps,user)
        if opc == 2:
            db.crear_tablas_csv(ps,user)
        if opc == 3:
            print("ejecutando visualizacion...")
            try:
                inicio.main()
            except KeyboardInterrupt:
                pass
        if opc == 4:
            print("saliendo...")
            os.remove('_Archivos/conexion.json')
            
        
if __name__ == "__main__":
    if conectar_basededatos():
        main()

    


    
    
    
    