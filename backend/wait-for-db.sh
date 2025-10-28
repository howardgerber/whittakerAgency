#!/bin/sh
# wait-for-db.sh - Wait for MariaDB to be ready

set -e

host="$1"
shift
cmd="$@"

until mysql -h"$host" -uwhittaker_user -pwhittaker_password_dev --skip-ssl -e 'SELECT 1' >/dev/null 2>&1; do
  >&2 echo "MariaDB is unavailable - sleeping"
  sleep 1
done

>&2 echo "MariaDB is up - executing command"
exec $cmd
