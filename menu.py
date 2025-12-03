from B_almacenamiento import database as db
from C_visualizacion import inicio
from mysql.connector import connect, Error
import json
import os
"""
Funcion para conctar a la base de datos
si no funciona cierra el programa
si si funciona crea un JSON para guardar los datos temporalmente, evitando asi, 
que el usuario tenga que introducir los mismos datos cada vez que quiera ejecutar una funcion
- No recibe parametros
- retorna un estado booleano, True si funciono la conexion, False si no funciono
"""
def conectar_basededatos():
    print("Es necesario tener la base de datos recursos_en_salud en MySQL")
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
"""
Menu principal, atravez de este se ejecutan todas las funciones
- No recibe parametros
- No retorna nada
"""
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

    


    
    
    
    