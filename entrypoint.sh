#!/bin/sh

python /code/project/manage.py collectstatic --no-input
python /code/project/manage.py migrate --no-input

exec "$@"
