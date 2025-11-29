from B_almacenamiento import database as db
from C_visualizacion import inicio


if __name__ == "__main__":
    
    print("NOTA. para ejecutar este programa, se debe crear previamente la base de datos\n'recursos_en_salud' en mySQL")
    opc =  0
    while opc != 4:
        opc = int(input("1. Crear tablas con webscrapper\n2. Crear tablas desde csv\n3. Dashboard\n4. salir\n"))
        if opc == 1:
            user = input("nombre de usuario: ")
            ps = input("contraseña de su servidor: ")
            db.crear_tablas_webscraper(ps,user)
        if opc == 2:
            user = input("nombre de usuario: ")
            ps = input("contraseña de su servidor: ")
            db.crear_tablas_csv(ps,user)
        if opc == 3:
            print("ejecutando visualizacion...")
            inicio.main()
        if opc == 4:
            print("saliendo...")
        