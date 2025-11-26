USE recursos_en_salud;

-- Relacion con tabla poblacion_total FK
ALTER TABLE recursos_en_salud.personal_salud_año
ADD CONSTRAINT fk_personal_año
FOREIGN KEY (Año)
REFERENCES recursos_en_salud.poblacion_total(Año);

-- Relacion con tabla estados FK
ALTER TABLE recursos_en_salud.personal_salud_año
ADD CONSTRAINT fk_personal_estado
FOREIGN KEY (ID_Estado)
REFERENCES recursos_en_salud.estados(ID);

-- Relacion con tabla poblacion_total FK
ALTER TABLE recursos_en_salud.poblacion_afiliada
ADD CONSTRAINT fk_afiliados_año
FOREIGN KEY (Año)
REFERENCES recursos_en_salud.poblacion_total(Año);

-- Relacion con tabla estado FK
ALTER TABLE recursos_en_salud.poblacion_afiliada
ADD CONSTRAINT fk_poblacion_estado
FOREIGN KEY (ID_Estado)
REFERENCES recursos_en_salud.estados(ID);

-- Relacion con tabla poblacion_total FK
ALTER TABLE recursos_en_salud.poblacion_derechohabiente
ADD CONSTRAINT fk_derechohabientes_año
FOREIGN KEY (Año)
REFERENCES recursos_en_salud.poblacion_total(Año);

-- Relacion con tabla instituciones FK 
ALTER TABLE recursos_en_salud.poblacion_derechohabiente
ADD CONSTRAINT fk_institucion_derechohabientes
FOREIGN KEY (ID_Institucion)
REFERENCES recursos_en_salud.instituciones(ID);

-- Relacion con tabla instituciones FK 
ALTER TABLE recursos_en_salud.personal_salud_institucion
ADD CONSTRAINT fk_personal_instituciones
FOREIGN KEY (ID_Institucion)
REFERENCES recursos_en_salud.instituciones(ID);

-- Relacion con tabla poblacion_total FK 
ALTER TABLE recursos_en_salud.personal_salud_institucion
ADD CONSTRAINT fk_poblacion
FOREIGN KEY (Año)
REFERENCES recursos_en_salud.poblacion_total(Año);









	


