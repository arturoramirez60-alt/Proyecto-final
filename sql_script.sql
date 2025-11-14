create database recursos_en_salud;
use recursos_en_salud;
show tables;

select * from poblacion_derechohabiente;
select * from poblacion_afiliada;
select * from personal_salud_año;
select * from personal_salud_institucion;
select * from poblacion_total;
select * from estados;
select * from instituciones;

drop database if exists recursos_en_salud;

#==============================================================================
#crear llaves primarias 

#estados
ALTER TABLE `recursos_en_salud`.`estados` 
CHANGE COLUMN `ID` `ID` BIGINT NOT NULL ,
ADD PRIMARY KEY (`ID`);
;

#instituciones
ALTER TABLE `recursos_en_salud`.`instituciones` 
CHANGE COLUMN `ID` `ID` BIGINT NOT NULL ,
ADD PRIMARY KEY (`ID`);
;

#personal_salud_año
ALTER TABLE `recursos_en_salud`.`personal_salud_año` 
CHANGE COLUMN `ID` `ID` BIGINT NOT NULL ,
ADD PRIMARY KEY (`ID`);
;

#personal_salud_institucion
ALTER TABLE `recursos_en_salud`.`personal_salud_institucion` 
CHANGE COLUMN `ID` `ID` BIGINT NOT NULL ,
ADD PRIMARY KEY (`ID`);
;

#poblacion afiliada
ALTER TABLE `recursos_en_salud`.`poblacion_afiliada` 
CHANGE COLUMN `ID` `ID` BIGINT NOT NULL ,
ADD PRIMARY KEY (`ID`);
;

#poblacion_derecho_habiente
ALTER TABLE `recursos_en_salud`.`poblacion_derechohabiente` 
CHANGE COLUMN `ID` `ID` BIGINT NOT NULL ,
ADD PRIMARY KEY (`ID`);
;

#poblacion_total
ALTER TABLE `recursos_en_salud`.`poblacion_total` 
CHANGE COLUMN `Año` `Año` BIGINT NOT NULL ,
ADD PRIMARY KEY (`Año`);
;

#================================================================================
#LLaves foraneas

#relacion poblacion_afiliada poblacion_total
ALTER TABLE poblacion_afiliada
ADD CONSTRAINT fk_poblacion_afiliada_año
FOREIGN KEY (Año)
REFERENCES poblacion_total(Año);

#relacion personal_salud_año poblacion?total

ALTER TABLE personal_salud_año;


select * from personal_salud_año;



