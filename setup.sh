#!/bin/bash
# setup script for vagrant
#

PROJECT_NAME=django-freeradmin

VENV_PATH=/var/local/venvs/$PROJECT_NAME

virtualenv $VENV_PATH
. $VENV_PATH/bin/activate
cd /vagrant
pip install -r requirements.txt

apt-get -qy install pwgen

PROFILE_FILE=/etc/profile.d/$PROJECT_NAME.sh
if [[ ! -e "$PROFILE_FILE" ]] ; then
  cat > $PROFILE_FILE <<-EOF
	DJANGO_FREERADMIN_DB_PWD=$(pwgen 9 1)
	DJANGO_FREERADMIN_DB_USER=djradius
	DJANGO_FREERADMIN_DB_NAME=djradius
	export DJANGO_FREERADMIN_DB_NAME DJANGO_FREERADMIN_DB_USER DJANGO_FREERADMIN_DB_PWD
EOF

fi
. $PROFILE_FILE

# setup DB
[[ -n "$DJANGO_FREERADMIN_DB_PWD" ]] || exit 1

echo "create database $DJANGO_FREERADMIN_DB_NAME" | mysql -pilikerandompasswords
echo "create user '$DJANGO_FREERADMIN_DB_USER'@'localhost' IDENTIFIED BY '$DJANGO_FREERADMIN_DB_PWD'" | mysql -pilikerandompasswords
echo "GRANT ALL ON $DJANGO_FREERADMIN_DB_NAME.* TO '$DJANGO_FREERADMIN_DB_USER'@'localhost'" | mysql -pilikerandompasswords
echo "FLUSH PRIVILEGES" | mysql -pilikerandompasswords
echo "password = $DJANGO_FREERADMIN_DB_PWD"

# setup django-freeradmin
mkdir -p /var/www/$PROJECT_NAME/{media,static}
cp djfreeradmin/settings.py.template djfreeradmin/settings.py
sed -i "s/^\(SECRET_KEY\).*$/\1 = '$( pwgen --secure 51 1 )'/" djfreeradmin/settings.py
python manage.py syncdb --noinput
python manage.py runserver 0.0.0.0:8000 &
