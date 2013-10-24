CREATE OR REPLACE VIEW radusergroup AS
  select g.id AS radgroup_id, u.username, g.groupname, g.priority
  from freeradmin_raduser u JOIN freeradmin_raduser_radgroups u2g on u.id=u2g.raduser_id
  JOIN freeradmin_radgroup g ON g.id=u2g.radgroup_id;

CREATE OR REPLACE VIEW radgroupcheck AS
  select  g2c.id, ug.groupname, c.attribute, c.op, c.value 
  from radusergroup ug 
  	JOIN freeradmin_radgroup_radchecks g2c ON ug.radgroup_id=g2c.radgroup_id
  	JOIN freeradmin_radcheck c on c.id=g2c.radcheck_id;

CREATE OR REPLACE VIEW radgroupreply AS
  select  g2r.id, ug.groupname, r.attribute, r.op, r.value 
  from radusergroup ug
  	JOIN freeradmin_radgroup_radreplies g2r ON ug.radgroup_id=g2r.radgroup_id
  	JOIN freeradmin_radreply r on r.id=g2r.radreply_id;
