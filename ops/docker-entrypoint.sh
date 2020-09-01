#!/bin/sh

export ENV_TYPE='local'
export PORT=8000

echo ENV_TYPE: ${ENV_TYPE}


# if [ "$DATABASE" = "postgres" ]; then
#     echo "Waiting for postgres..."

#     #psql -h ${DATABASE_HOST} -U postgres -c "SELECT 1 FROM pg_database WHERE datname = " + ${POSTGRES_DB} | grep -q 1 || psql -h ${DATABASE_HOST} -U postgres -c "CREATE DATABASE " + ${POSTGRES_DB}

#     while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
#       sleep 0.1
#     done

#     echo "PostgreSQL started"
# fi

#uwsgi --ini /etc/uwsgi/uwsgi.ini


# Make migrations and migrate the database.
echo "Making migrations and migrating the database. "
python3 manage.py makemigrations --noinput 
python3 manage.py migrate --noinput
#python3 manage.py runserver #localhost:${PORT}
exec "$@"