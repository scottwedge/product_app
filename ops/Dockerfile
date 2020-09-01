# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

EXPOSE 8080/tcp

#CMD snap remove docker, rm -R /var/lib/docker, sudo apt-get remove docker docker-engine docker.io

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1


RUN apt-get update && apt-get install -y netcat uwsgi uwsgi-plugin-python uwsgi-plugin-cgi libapache2-mod-uwsgi

# Create an app user 
RUN useradd --user-group --create-home --no-log-init --shell /bin/bash app

ENV PROJECT_DIR /Apps

COPY . ${PROJECT_DIR}
COPY ./ops/docker-entrypoint.sh /usr/bin
RUN chmod +x /usr/bin/docker-entrypoint.sh

WORKDIR ${PROJECT_DIR}

# RUN chown -R app:app ${PROJECT_DIR}

# USER app:app

# # Upgrade pip
# RUN pip install --upgrade pip

# # Install the requirements.

RUN python -m pip install -r requirements.txt

#CMD sudo service postgresql status
#CMD init-database.sh

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
# RUN useradd appuser && chown -R appuser /Apps
# USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# File wsgi.py was not found in subfolder:products_app. Please enter the Python path to wsgi file.

#CMD sudo /etc/init.d/nginx restart, ["gunicorn", "--bind", "0.0.0.0:8000", "products_app.backend.wsgi"]
CMD sudo /etc/init.d/nginx restart
ENTRYPOINT ["docker-entrypoint.sh"]



# FROM python:3.8-slim-buster

# ENV PYTHONBUFFERED 1
# ENV PYTHONWRITEBYTECODE 1

# RUN apt-get update \
#     && apt-get install -y netcat

# # Create an app user 
# RUN useradd --user-group --create-home --no-log-init --shell /bin/bash app

# ENV APP_HOME=/home/app/web

# # Create the staticfiles directory. This avoids permission errors. 
# #RUN mkdir -p $APP_HOME/staticfiles

# WORKDIR $APP_HOME

# COPY requirements.txt $APP_HOME
# RUN pip install --upgrade pip 
# RUN python -m pip install -r requirements.txt

# COPY . $APP_HOME

# RUN chown -R app:app $APP_HOME

# USER app:app

# ENTRYPOINT ["/home/app/web/ops/docker-entrypoint.sh"]