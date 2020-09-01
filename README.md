# Product APP Project

## Instructions

* VS code Extensions:

I recommand the below:
1 Docker
2 Better comments
3 Python (Linting, Debugging (multi-threaded, remote), Intellisense, Jupyter Notebooks, code formatting, refactoring, unit tests, snippets, and more.)
4 Indent Rainbow

Install and configure Python environment.
    Ideally [Anaconda](https://www.anaconda.com/download/).

* Install Docker locally

* Setup Run configuration

* Login to Docker in order to run parts of the environment locally

```bash
docker login
```

* Clone the Git repository

```bash
git clone git@github.com:sbenou/portal-product_app.git
cd product_app
git config user.email “name.last_name@email.com”
git config user.name “Name LastName”
```

* Install all the dependencies. Make sure this is the same pip that belongs to python you've used in IDE

```bash
pip install -r requirements.txt
```

* Declare system variables
Ideally place them under system variables

```bash
ENV_TYPE=local
```

* [OPTIONAL] Run local services if you don't wish to use team-shared Dev environment:

```bash
# Change directory to Git root
cd "$(git rev-parse --show-toplevel)"

# all services:
docker-compose up -d
```

* Check which containers was started:

```bash
docker-compose ps
```

* [OPTIONAL] Halt the services:

```bash
docker-compose down
```

* Migrations:
Database in Dev environment is SQLite. It will automatically be created under database subdirectory.
But you have to populate it yourself. Make sure you use same python as configured in IDE.

```bash
python manage.py migrate
```

* APIs
Now you can Run the application and connect to [http://localhost:8000/api/graphql](http://localhost:8000/api/graphql)

Better yet, you can download [Insomnia](https://insomnia.rest/download/) to test the Backend functionalit. All you have to do is install it and create a new environment
and import the file which is the 'enpoints' folder in this project. You will then be able to test each query and mutation.

## Create new Apps

* to create a new app within the app folder:

1. create a new folder with the app name

2. Apply:

```bash
python manage.py startapp <new_app_name> ./backend/Apps/<new_app_name>
```

## Fixtures

A directory for fixtures has been added in the settings file (FIXTURES_DIRS) so we can create fixtures
and load data from fixtures from any app.

Now that we have 2 databases in the project and that we are using databaserouters, when creating fixtures
we need to specify the database we are going to use as shown in the example below:

``` bash
python manage.py dumpdata user --indent 4 > backend/Apps/user/fixtures/initial_data.json
```

now loading fixtures from a file to the database:

```bash
python manage.py loaddata fixtures/initial_data.json --app <app.model_name>

```

## Tests

Before running the tests run:

```bash
export DJANGO_SETTINGS_MODULE=backend.settings.testing
```

then run:

```bash
py.test -s
```
