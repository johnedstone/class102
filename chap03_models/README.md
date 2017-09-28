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
