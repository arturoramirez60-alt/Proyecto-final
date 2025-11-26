show tables;

select * from estados;
select * from instituciones;
select * from personal_salud_año;
select * from personal_salud_institucion;
select * from poblacion_afiliada;
select * from poblacion_derechohabiente;
select * from poblacion_total;

call sp_personal_salud_año();
call sp_personal_salud_institucion();
call sp_poblacion_afiliada();
call sp_poblacion_derechohabiente();
call sp_poblacion();
