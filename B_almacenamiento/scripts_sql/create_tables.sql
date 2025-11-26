
CREATE DATABASE IF NOT EXISTS recursos_en_salud;
USE recursos_en_salud;

-- TABLA 1: poblacion_total
CREATE TABLE IF NOT EXISTS poblacion_total (
    Año INT NOT NULL PRIMARY KEY,
    Poblacion INT,
);


-- TABLA 2: estados
CREATE TABLE IF NOT EXISTS estados (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Estado VARCHAR(100),
);


-- TABLA 3: instituciones
CREATE TABLE IF NOT EXISTS instituciones (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Institucion VARCHAR(100),

);


-- TABLA 4: poblacion_afiliada
CREATE TABLE IF NOT EXISTS poblacion_afiliada (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ID_Estado INT,
    Porcentaje DOUBLE,
    Año INT,
);


-- TABLA 5: poblacion_derechohabiente
CREATE TABLE IF NOT EXISTS poblacion_derechohabiente (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ID_Institucion INT,
    Porcentaje DOUBLE,
    Año INT,
);


-- TABLA 6: personal_salud_año
CREATE TABLE IF NOT EXISTS personal_salud_año (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Año INT,
    Medicos_generales_especialistas_y_odontologos INT,
    Personal_medico_en_formacion INT,
    Medicos_en_otras_labores INT,
    Enfermeras_generales_y_especialistas INT,
    Pasantes_de_enfermeria INT,
    Auxiliares_de_enfermeria INT,
    Personal_de_enfermeria_en_otras_labores INT,
    Personal_profesional INT,
    Personal_tecnico INT,
    Otro_personal INT,
    TOTAL INT,
    ID_Estado INT,
);


-- TABLA 7: personal_salud_institucion

CREATE TABLE IF NOT EXISTS personal_salud_institucion (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ID_Institucion INT,
    total INT,
    Año INT,
);

