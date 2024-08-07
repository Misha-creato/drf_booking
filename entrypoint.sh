#!/bin/bash

if [ -z "$DEBUG" ]; then
  DEBUG=True
fi

if [ "$DEBUG" = "True" ]; then
  echo "Debug mode is ON. Executing debug commands..."
  python manage.py runserver 127.0.0.1:8000
else
  echo "Debug mode is OFF. Executing production commands..."
  python manage.py collectstatic --noinput&
  python manage.py migrate&
  redis-server&
  sudo supervisord -n -c supervisord.conf
fi
