### Introducing Models.

This chapter does not depend on any setup from the previous chapters.
Introducing how to use python 3.x on Centos/RedHat Linux. This chapter
should work on both python 2.7 and 3.x.

Also introducing the django debug toolbar.  And, to get this to work we will be
running the server locally, and using ssh with port forwading.  If you don't care
about the debug tool, you can continue to use 0.0.0.0:8080 and set `ALLOWED_HOST=['*']`

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
