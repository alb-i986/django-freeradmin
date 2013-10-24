CREATE OR REPLACE VIEW radcheck AS
  select  c.id, u.username, c.attribute, c.op, c.value 
  from freeradmin_raduser u join freeradmin_raduser_radchecks a on u.id =a.raduser_id join freeradmin_radcheck c on c.id=a.radcheck_id;
