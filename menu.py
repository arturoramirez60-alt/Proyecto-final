import bases_de_datos as db


if __name__ == "__main__":
    
    print("NOTA. para ejecutar este programa, se debe crear previamente la base de datos\n'recursos_en_salud' en mySQL")
    opc =  0
    while opc != 3:
        opc = int(input("1. Crear tablas con webscrapper\n2. Crear tablas desde csv\n3. salir\n"))
        if opc == 1:
            ps = input("contraseña de su servidor: ")
            db.crear_tablas_webscraper(ps)
        if opc == 2:
            ps = input("contraseña de su servidor: ")
            db.crear_tablas_csv(ps)
        