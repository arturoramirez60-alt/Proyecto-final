import bases_de_datos as db


if __name__ == "__main__":
    
    opc =  0
    while opc != 3:
        opc = int(input("1. Crear tablas con webscrapper\n2. Crear tablas desde csv\n3. salir\n"))
        
        if opc == 1:
            contraseña =  input("contraseña: ")
            db.crear_tablas_webscraper(contraseña)
        if opc == 2:
            db.crear_tablas_csv()
        