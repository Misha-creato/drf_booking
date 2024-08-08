#!/bin/bash

if [ -z "$DEBUG" ]; then
  DEBUG=True
fi

if [ -z "$HOST" ]; then
  HOST='0.0.0.0'
fi

if [ -z "$PORT" ]; then
  PORT='8000'
fi

if [ -z "$WORKERS" ]; then
  WORKERS=3
fi

python manage.py migrate

if [ "$DEBUG" = "True" ]; then
  echo "Debug mode is ON. Executing debug commands..."
  python manage.py runserver $HOST:$PORT
else
  echo "Debug mode is OFF. Executing production commands..."
  python manage.py collectstatic --noinput&
  gunicorn -c gunicorn.conf.py --bind=$HOST:$PORT --workers=$WORKERS
fi
