django-freeradmin
=================

Custom web based administration interface for the freeradius radius server, specifically designed for MAC authentication.

Heavily exploiting the powerful and lovely Django (1.5) admin app: not a single line of HTML written, it's all in Model and ModelAdmin definitions.

Inspired by http://git.io/4kWEZA



Goals
-----

We are using the freeradius server for MAC authentication, so we needed an administrative interface more modern and intuitive than the official `dialup-admin`. One which could possibly use foreign keys, by the way.



Features: operations
--------------------

- CRUD radchecks (attribute-op-value triples the radius server checks when a request comes in)
- CRUD radreplies (attribute-op-value triples sent by the radius server in reply to client requests)
- CRUD VLANs
- CRUD users (MAC addresses) (including the associations with radchecks, radreplies and VLANs)
- CRUD groups



Setup
-----

Django setup
^^^^^^^^^^^^

1. Clone/download this repo (it's a full Django project, btw)
2. Copy settings.py.template to settings.py (an unversioned file) and customize your settings
3. `pip install -r .REQ`
4. `./manage.py syncdb` (which also installs a fixture with some sample data)
5. `./manage.py runserver`

Integrating django-freeradmin with Freeradius server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since the resulting schema of the DB for this project is different (better, IMHO) from the default (MySQL) schema that comes with freeradius, we need to customize some parameters in the configuration of freeradius:

1. edit /etc/freeradius/sql.conf and customize the names of the tables [..] (TODO)
2. edit /etc/freeradius/sql/mysql/dialup.conf and customize the SQL queries [..] (TODO)



Notes
-----

It is not possible to create a radreply with the attribute `Extreme-Netlogin-Vlan` because this attribute is handled internally by the system. Instead, you should associate a VLAN object to the raduser.



Extensions
----------

We were concerned with a minimal MAC authentication, so our solution does not include concepts like accounting, radpostauth, and so on.
If you are also interested in the other rad* tables, then have a look at http://git.io/4kWEZA
