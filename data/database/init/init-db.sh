#!/bin/bash
set -e

# Create domain schemas
for SCHEMA in music entertainment weather gaming development productivity general; do
  echo "Creating schema $SCHEMA..."
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE SCHEMA IF NOT EXISTS $SCHEMA;
EOSQL
done
