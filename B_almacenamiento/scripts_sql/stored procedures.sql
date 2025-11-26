USE recursos_en_salud;

#procedure para personal_salud_año
delimiter $$
create procedure sp_personal_salud_año() 
begin
	select 
        psa.*, e.Estado, pt.Poblacion as Poblacion_total
	from personal_salud_año as psa 
	left join estados as e on e.ID = psa.ID_Estado
	left join poblacion_total as pt on psa.Año = pt.Año;
end $$
delimiter ;
call sp_personal_salud_año();


#procedure para personal_salud_institucion
delimiter $$
create procedure sp_personal_salud_institucion() 
begin
	select psi.ID, pa.Año, i.Institucion, psi.total as Personal_total,pa.poblacion as poblacion_total from  personal_salud_institucion as psi
	left join instituciones as i on i.ID = psi.ID_institucion
    left join poblacion_total as pa on pa.Año = psi.Año;
end $$
delimiter ;
call sp_personal_salud_institucion();


#procedure para poblacion_afiliada
delimiter $$
create procedure sp_poblacion_afiliada() 
begin
select pa.ID, e.Estado, pa.Año,pt.Poblacion, pa.Porcentaje as Procentaje_afiliado from poblacion_afiliada as pa
left join estados as e on e.ID = pa.ID_Estado
left join poblacion_total as pt on pa.Año = pt.Año;
end $$
delimiter ;
call sp_poblacion_afiliada();

#procedures para poblacion_derechohabiente
delimiter $$
create procedure sp_poblacion_derechohabiente() 
begin
select pdh.ID,i.institucion,pdh.Año,pt.Poblacion as Poblacion_total,pdh.Porcentaje as Porcentaje_afiliado from poblacion_derechohabiente as pdh
left join instituciones as i on i.ID = pdh.ID_institucion
left join poblacion_total as pt on pdh.Año = pt.Año;
end $$
delimiter ;
call sp_poblacion_derechohabiente();

#procedure para poblacion__total
delimiter $$
create procedure sp_poblacion() 
begin
	select * from poblacion_total;
end $$
delimiter ;
call sp_poblacion_total();

