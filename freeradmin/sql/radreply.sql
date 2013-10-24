CREATE OR REPLACE VIEW radreply AS 

  SELECT r.id, u.username, r.attribute, r.op, r.value 
  FROM freeradmin_raduser u join freeradmin_raduser_radreplies a on u.id=a.raduser_id
       JOIN freeradmin_radreply r ON r.id=a.radreply_id

    UNION

  SELECT r.id, u.username, r.attribute, r.op, r.value
  FROM freeradmin_raduser u JOIN freeradmin_radreply r on u.vlan_id=r.id;