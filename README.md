django-freeradmin
=================

Custom web based administration interface for the freeradius radius server, specifically designed for MAC authentication.

Heavily exploiting the powerful and lovely Django (1.5) admin app: not a single line of HTML written, it's all in Model and ModelAdmin definitions.

Inspired by http://git.io/4kWEZA



Goals
-----

We use the freeradius server for MAC authentication, so we needed an administrative interface more modern and intuitive than the official `dialup-admin`. One which could possibly use foreign keys, by the way.



Features: operations
--------------------

- CRUD radreplies (attribute-op-value triples sent by the radius server in reply to client requests)
- CRUD VLANs
- CRUD MAC addresses (including associating radreplies and VLANs to MAC addresses)



Setup
-----

Django setup
^^^^^^^^^^^^

1. Clone/download this repo (it's a full Django project, btw)
2. Copy settings.py.template to settings.py (an unversioned file) and customize your settings
3. `pip install -r .REQ`
4. `./manage.py syncdb` (it also installs a fixture with some sample data)
5. `./manage.py runserver`

Integrating django-freeradmin with Freeradius server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since the schema of the DB is different (better, IMHO) from the default (MySQL) schema that comes with freeradius, we need to perform the customize some parameters in the configuration of freeradius:

1. edit /etc/freeradius/sql.conf and customize the names of the tables radcheck and radreply, replacing their names with `freeradmin_radcheck` and `freeradmin_radreply`
2. edit /etc/freeradius/sql/mysql/dialup-conf and customize the SQL queries `authorize_check_query` and `authorize_reply_query`

Alternatively, you could create a view in the DBMS simulating the original schema.



Extensions
----------

We concentrated on the MAC authentication, so we just included the tables radcheck and radreply, on purpose.
If you also need the other tables as radusergroup, radpostauth, etc, then have a look at http://git.io/4kWEZA



Notes
-----

It is not possible to create a radreply with attribute `Extreme-Netlogin-Vlan` because this attribute is handled internally by the system. Instead, you should associate a VLAN object to the radcheck object.