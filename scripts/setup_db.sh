#!/usr/bin/env bash
# Create (or recreate) the database and load schema, functions, roles and data.
#   scripts/setup_db.sh [dbname]        uses PG* environment variables for the connection
set -euo pipefail
DB=${1:-pharmacy}
cd "$(dirname "$0")/.."
dropdb --if-exists "$DB"
createdb "$DB"
for f in sql/01_schema.sql sql/02_functions.sql sql/03_roles.sql sql/04_seed.sql; do
    psql -v ON_ERROR_STOP=1 -q -d "$DB" -f "$f"
done
echo "database '$DB' ready"
