### Introducing Models.

This chapter does not depend on any setup from the previous chapters.
Introducing how to use python 3.x on Centos/RedHat Linux. This chapter
should work on both python 2.7 and 3.x.

Also introducing the django debug toolbar.  And, to get this to work we will be
running the server locally, and using ssh with port forwading.  If you don't care
about the debug tool, you can continue to use 0.0.0.0:8080 and set `ALLOWED_HOST=['*']`

### References
* https://docs.djangoproject.com/en/1.11/intro/tutorial01/

### Setup

```
# Enter the SCL environment and set up virtualenv
scl enable rh-python35 bash
virtualenv-3.5 ~/.virtualenvs/chap03
env |egrep LD_LIBRARY

# Output:
LD_LIBRARY_PATH=/opt/rh/rh-python35/root/usr/lib64

# Exit SCL env
exit

# Use new virtualenv w/o SCL by exporting LD_LIBRARY
source ~/.virtualenvs/chap03/bin/activate
export LD_LIBRARY_PATH=/opt/rh/rh-python35/root/usr/lib64

export PIP_PROXY=<ip:port>
pip install --proxy ${PIP_PROXY} pip --upgrade
pip install --proxy ${PIP_PROXY} django django-debug_toolbar
cd class102/chap03_models/
echo '# python 3.5' > requirements.txt
pip freeze |egrep -i 'django|debug' | tee -a requirements.txt

# Output:
Django==1.11.5
django-debug-toolbar==1.8

pwd
# Output
class102/chap03_models
tree
.
`-- requirements.txt

0 directories, 1 file
```

### Start django project and app
```
pwd
class102/chap03_models

django-admin startproject chap3_project
cd chap3_project/
django-admin startapp chap3_app

tree ../
../
|-- chap3_project
|   |-- chap3_app
|   |   |-- admin.py
|   |   |-- apps.py
|   |   |-- __init__.py
|   |   |-- migrations
|   |   |   `-- __init__.py
|   |   |-- models.py
|   |   |-- tests.py
|   |   `-- views.py
|   |-- chap3_project
|   |   |-- __init__.py
|   |   |-- settings.py
|   |   |-- urls.py
|   |   `-- wsgi.py
|   `-- manage.py
|-- README.md
`-- requirements.txt
```


### What is the current working directory?
Most of the following is run from `class102/chap03_models/chap3_project`

### More setup
* Move wsgi for openshift
* setup settings and template for openshift

```
mv chap3_project/wsgi.py .
```

* Update `chap3_project/{settings,urls}.py` as of tag v0.1, then run these commands

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

# and view in browser after first tunnelling - notice toolbar
# ssh -x -C -L 8000:127.0.0.1:8000 user@fqdn
# or runserver at 0.0.0.0:8000 and miss seeing the debug toolbar
```

### Setup models.py: tag v0.2
Note: All of the above was done at tag v0.1

* update chap3_app/{models,admins}.py as in tag v0.2
* Then
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

* runserver and go to http://127.0.0.1:8000/admin/ and add two users and two servers
* Also explore the django shell

```
python manage.py shell
>>> from chap3_app.models import Server
>>> s = Server.objects.all()
>>> for ea in s:
...     print(ea.pk, ea.ip, ea.user, ea.user.username)
...
1 4.4.4.4 userone userone
2 8.8.8.8 usertwo usertwo
```

#### More python shell, for fun
```
python manage.py shell
>>> from django.contrib.auth.models import User
>>> u = User(username="userthree")
>>> u.full_clean()
Traceback (most recent call last):
  django.core.exceptions.ValidationError: {'password': ['This field cannot be blank.']}
# okay
>>> u.save()

>>> from chap3_app.models import Server
>>> s = Server()
>>> s.user =u
>>> s.name = 'serverthree'
>>> s.ip = 8
>>> s.full_clean()
Traceback (most recent call last):
django.core.exceptions.ValidationError: {'ip': ['Enter a valid IPv4 address.']}
>>> s.ip = '8.8.4.4'
>>> s.full_clean()
>>> s.save()
```

### Setup views and templating: tag v0.3
* update chap3_app/{views,urls}.py
* update chap3_project/urls.py
* copy chap3_app/{templates,static} directory
* then runserver

```
python manage.py runserver
```

### Add login: tag v0.4

* Prepare for authentication and eventually Openshift
```
pwd
class102/chap03_models/chap3_project

pip install --proxy ${PIP_PROXY} django-bootstrap-form whitenoise gunicorn

pip freeze | egrep -i 'bootstrap|whitenoise|gunicorn' | tee -a ../requirements.txt
django-bootstrap-form==3.3
whitenoise==3.3.1

```

* Grab a fresh copy of chap3_project/{settings,urls}.py from v0.4
* Grab a fresh copy of chap3_app/{urls, views}.py from v0.4
* Grab a fesh copy of the templates base.html, server_list.html, add the 404.html and login.html, and grab private html from v0.4

```
python manage.py runserver
```

* Files as of v0.4
```
 tree -I "*pyc" -I "*cache*"  ../
../
|-- chap3_project
|   |-- chap3_app
|   |   |-- admin.py
|   |   |-- apps.py
|   |   |-- __init__.py
|   |   |-- migrations
|   |   |   |-- 0001_initial.py
|   |   |   `-- __init__.py
|   |   |-- models.py
|   |   |-- static
|   |   |   `-- css
|   |   |       `-- style.css
|   |   |-- templates
|   |   |   |-- 404.html
|   |   |   |-- base.html
|   |   |   |-- chap3_app
|   |   |   |   |-- private.html
|   |   |   |   `-- server_list.html
|   |   |   `-- login.html
|   |   |-- tests.py
|   |   |-- urls.py
|   |   `-- views.py
|   |-- chap3_project
|   |   |-- __init__.py
|   |   |-- settings_orig.py
|   |   |-- settings.py
|   |   `-- urls.py
|   |-- db.sqlite3
|   |-- manage.py
|   `-- wsgi.py
|-- README.md
`-- requirements.txt
```

#### Test for Production

```
export ALLOWED_HOSTS='*' DEBUG=off
python manage.py runserver
python manage.py runserver

# Test a bad url in browser and see if the custom 404.html along with response of 404 is working
# Then
unset ALLOWED_HOSTS
unset DEBUG
```

### Deploy on Openshift: v0.5

* mv requirements.txt in one directory for Openshift

```
pwd
class102/chap03_models/chap3_project
mv ../requirements.txt .

tree -I "*pyc" -I "*cache*"  ../
../
|-- chap3_project
|   |-- chap3_app
|   |   |-- admin.py
|   |   |-- apps.py
|   |   |-- __init__.py
|   |   |-- migrations
|   |   |   |-- 0001_initial.py
|   |   |   `-- __init__.py
|   |   |-- models.py
|   |   |-- static
|   |   |   `-- css
|   |   |       `-- style.css
|   |   |-- templates
|   |   |   |-- 404.html
|   |   |   |-- base.html
|   |   |   |-- chap3_app
|   |   |   |   |-- private.html
|   |   |   |   `-- server_list.html
|   |   |   `-- login.html
|   |   |-- tests.py
|   |   |-- urls.py
|   |   `-- views.py
|   |-- chap3_project
|   |   |-- __init__.py
|   |   |-- settings_orig.py
|   |   |-- settings.py
|   |   `-- urls.py
|   |-- db.sqlite3
|   |-- manage.py
|   |-- openshift
|   |   `-- templates
|   |       `-- non_prod.yaml
|   |-- openshift_parameters.sh
|   |-- requirements.txt
|   `-- wsgi.py
`-- README.md


```

* update chap3_project/{settings,urls}.py
* take a look at `openshift_parameters.sh` file
* take a look at openshift/templates/{non_prod,prod}.yaml
* notice there is a custom `.s2i/bin/run` script to create a superuser upon deployment
* Deploy in Openshift

```
oc new-project userid-class102
oc new-app --param-file openshift_parameters.sh -f openshift/templates/non_prod.yaml
oc logs bc/class102-chap3 -f
oc logs dc/class102-chap3 -f
oc get pods
```
