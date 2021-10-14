#!/bin/sh

cd project
python manage.py collectstatic --no-input
python manage.py migrate --no-input

exec "$@"
