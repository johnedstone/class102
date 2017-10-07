### Purpose
* Chapter 5 builds on the ideas presented in chapter 4, using PostgreSQL
* Add json fields to allow json dictionaries for tags by clients
* Start tagging at v5.01

### Tag v5.01 in progress ..
* Reduce models to just AWS S3 create bucket
* Create new templates with v5.xx tagging
* Added pip psycopg2
* change str(response)field to json

#### Notes on running postgresql locally for development

```
## Add these to environment
## Some are for django, some are for the postgresql pod
export DATABASE_SERVICE_NAME=postgresql
export DATABASE_ENGINE=postgresql
export DATABASE_NAME=db_name
export DATABASE_USER=db_user
export DATABASE_PASSWORD=db_password

# Create postgresql running instance with this command
oc new-app -p POSTGRESQL_USER=${DATABASE_USER} \
           -p POSTGRESQL_PASSWORD=${DATABASE_PASSWORD} 
           -p POSTGRESQL_DATABASE=${DATABASE_NAME} 
           -f openshift/templates/postgresql-ephemeral.yaml

# Open another window where HTTP(S)_PROXY is NOT set and do port-forwarding
oc port-forward <pod> 5432

# Now return to the first window and run these two commands
python manage.py migrate
python manage.py runserver
python manage.py set_client_token boohoo boohoowoohoo

# Then curl or httpie the API endpoint

# Cleaning up PostgreSQL project
oc delete all --all
oc delete secrets postgresql

```
