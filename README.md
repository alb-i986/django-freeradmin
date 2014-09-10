django-freeradmin
=================

Custom web based administration interface for the freeradius radius server, specifically designed for MAC authentication.

Heavily exploiting the powerful and lovely Django (1.5) admin app: not a single line of HTML written, it's all in Model and ModelAdmin definitions.

Inspired by http://git.io/4kWEZA



Goals
-----

We are using the freeradius server for MAC authentication, and we needed an administrative interface more modern and intuitive than the official `dialup-admin`. One which could possibly make use of foreign keys, by the way.



Features: operations
--------------------

- CRUD radchecks (attribute-op-value triples the radius server checks when a request comes in)
- CRUD radreplies (attribute-op-value triples the radius server sends in reply to client requests), 
- CRUD VLANs
- CRUD groups,
- CRUD users (MAC addresses, in our context) (including the associations with groups, radchecks, radreplies and VLANs)



Setup
-----

First of all, you need to copy settings.py.template to settings.py (which is unversioned) and customize it with your own settings.
In the DB settings, please make sure to configure the very DB Freeradius is querying.

### Vagrant way
See also https://github.com/alb-i986/vagrantfiles

Drawback: it has [a few requirements](https://github.com/alb-i986/vagrantfiles#requirements).

Once you have them all:

1. run `vagrant up`
2. open your browser and go to http://localhost:8000/
3. Login as 'admin', password 'admin'

### Manual way

1. `pip install -r requirements.txt`
2. `./manage.py syncdb` (which installs a fixture and custom SQL scripts)
3. `./manage.py runserver`
4. open your browser and go to http://localhost:8000/
5. Login as 'admin', password 'admin'

The fixture at step 2 installs:
- a super user 'admin', whose password is 'admin'
- a group 'MAC Admin', granted with privileges to CRUD MAC addresses
- a user 'mac_admin', whose password is 'admin', belonging to the group 'MAC Admin'
- some sample data


Implementation
--------------

### DB schema

I wanted to make things clean, so the app was designed following Django defaults and style, which means that the DB schema is way different (better, IMHO) from the original one (at least, from what is in `freeradius-mysql` Debian's package).



### Integration with Freeradius server

Despite the different SQL schema, django-freeradmin happens to be integrated with Freeradius server thanks to the SQL Views that are defined in custom SQL scripts (see `freeradmin/sql/*.sql`), which abstract the differences.



Extensions
----------

We were concerned with a minimal MAC authentication, so our solution does not include concepts like accounting, radpostauth, and so on.
If you are also interested in the other rad* tables, then you should probably have a look at http://git.io/4kWEZA.
