#!/bin/bash

# Ждем готовности PostgreSQL (без netcat)
echo "Waiting for PostgreSQL..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    # Используем Python для проверки подключения
    if python -c "
import sys
import psycopg2
from psycopg2 import OperationalError
try:
    # Эти переменные берутся из .env через docker-compose
    conn = psycopg2.connect(
        host='postgres',
        dbname='$DATABASE_NAME',
        user='$DATABASE_USERNAME',
        password='$DATABASE_PASSWORD',
        port=5432,
        connect_timeout=3
    )
    conn.close()
    sys.exit(0)
except OperationalError as e:
    print(f'Connection attempt {sys.argv[1] if len(sys.argv) > 1 else attempt}: {e}')
    sys.exit(1)
" "$attempt"; then
        echo "PostgreSQL is ready!"
        break
    fi
    
    echo "Attempt $attempt/$max_attempts: PostgreSQL not ready, waiting..."
    sleep 2
    attempt=$((attempt + 1))
    
    if [ $attempt -gt $max_attempts ]; then
        echo "ERROR: PostgreSQL not ready after $max_attempts attempts!"
        exit 1
    fi
done

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Checking if database needs initial data..."
if python manage.py shell -c "
from django.contrib.auth.models import User
if User.objects.exists():
    print('Database has users, skipping loaddata')
    exit(0)
else:
    print('Database is empty, will load data')
    exit(1)
" 2>/dev/null; then
    echo "Database already has data, skipping loaddata"
else
    echo "Loading initial data from db.json..."
    if [ -f "db.json" ]; then
        python manage.py loaddata db.json
        echo "Data loaded successfully"
    else
        echo "Warning: db.json not found, skipping loaddata"
    fi
fi

echo "Starting Django server..."
exec "$@"