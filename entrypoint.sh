#!/bin/sh

if [ ! -z "$DB_HOST" ] && [ ! -z "$DB_PORT" ]; then
  # Waiting for database connection

  while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.2
  done
fi

exec "$@"
