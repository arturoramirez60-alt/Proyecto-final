from B_almacenamiento import database as db
from C_visualizacion import inicio
from mysql.connector import connect, Error
import json
import os



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

            
        
if __name__ == "__main__":
    main()

    


    
    
    
    