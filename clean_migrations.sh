
#!/bin/sh

echo "initializing migrations clean up process ..."

#py manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json

#echo "dumping database data into db.json"
#sleep 0.5

echo " cleaning up migration files ..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

echo "resetting database"
mv -u -v  backend/database/db.sqlite3 backend/database/db.sqlite3.old

echo "running migrations..."

py manage.py makemigrations
py manage.py migrate

#echo "loading fixtures data into database ..."
#py manage.py loaddata db.json

echo "migrations clean up process completed .. running server..."

python manage.py runserver