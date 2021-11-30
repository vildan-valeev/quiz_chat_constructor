#!/usr/bin/env sh

#if [ "$DATABASE" = "postgres" ]
#then
#    echo "Waiting for postgres..."
#
#    while ! nc -z $SQL_HOST $SQL_PORT; do
#      sleep 0.1
#    done
#
#    echo "PostgreSQL started"
#fi

#python manage.py flush --no-input
#python manage.py makemigrations --no-input  # del after first run
python manage.py migrate --no-input
python manage.py runserver 0.0.0.0:8000

#exec "$@"
