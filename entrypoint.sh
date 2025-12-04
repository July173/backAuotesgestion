#!/bin/sh
set -e

echo "Waiting for database at ${DB_HOST}:${DB_PORT:-3306}..."

# If DB host and user are provided, wait until MySQL is reachable
if [ -n "$DB_HOST" ] && [ -n "$DB_USER" ]; then
  until mysqladmin ping --ssl=FALSE -h "$DB_HOST" -u"$DB_USER" -p"$DB_PASS" >/dev/null 2>&1; do
    echo "MySQL is unavailable - sleeping"
    sleep 2
  done
fi

echo "Database ready — running migrations"
# Create migrations (if any) and apply them only when RUN_MIGRATIONS is true.
if [ "${RUN_MIGRATIONS:-false}" = "true" ]; then
  echo "RUN_MIGRATIONS=true — applying migrations"
  python manage.py makemigrations --noinput || true
  python manage.py migrate --noinput
else
  echo "RUN_MIGRATIONS not true — skipping migrations"
fi

echo "Starting process: $@"
exec "$@"
