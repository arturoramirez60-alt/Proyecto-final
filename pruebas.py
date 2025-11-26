from A_extraccion import limpieza as li


if __name__ == "__main__":
    df = li.limpiar_personal_salud_institucion()
    print(df)