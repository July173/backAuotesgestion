#!/bin/sh
set -e

MAX_TRIES=60
SLEEP_SECONDS=2

echo "Waiting for database at ${DB_HOST}:${DB_PORT:-3306} and for migrations to be applied..."

i=0
while [ $i -lt $MAX_TRIES ]; do
  if mysql --ssl=FALSE -h "${DB_HOST}" -u"${DB_USER}" -p"${DB_PASS}" -e "SELECT COUNT(*) FROM ${DB_NAME}.django_migrations;" >/dev/null 2>&1; then
    COUNT=$(mysql --ssl=FALSE -h "${DB_HOST}" -u"${DB_USER}" -p"${DB_PASS}" -sN -e "SELECT COUNT(*) FROM ${DB_NAME}.django_migrations;") || COUNT=0
    if [ "${COUNT}" -gt 0 ]; then
      echo "Detected applied migrations (count=${COUNT}). Continuing."
      exit 0
    fi
  fi
  i=$((i+1))
  echo "Migrations not applied yet (${i}/${MAX_TRIES})... sleeping ${SLEEP_SECONDS}s"
  sleep ${SLEEP_SECONDS}
done

echo "Timeout waiting for migrations after $((MAX_TRIES * SLEEP_SECONDS))s" >&2
exit 1
