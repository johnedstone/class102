### Usage
#### Setup 
```
mkdir standard_django_hello_world
cd standard_django_hello_world/
virtualenv ~/.virtualenvs/standard_django_hello_world
source ~/.virtualenvs/standard_django_hello_world/bin/activate
export PIP_PROXY=<ip:port>
pip install --proxy ${PIP_PROXY} pip --upgrade
pip install --proxy ${PIP_PROXY} django
echo "# python2.7" > requirements.txt
pip freeze | egrep -i django | tee -a requirements.txt 
```

#### Django setup
```
django-admin startproject myproject
django-admin startapp myapp
```
##### Current layout
```
|-- myapp
|   |-- admin.py
|   |-- apps.py
|   |-- __init__.py
|   |-- migrations
|   |   `-- __init__.py
|   |-- models.py
|   |-- tests.py
|   `-- views.py
|-- myproject
|   |-- db.sqlite3
|   |-- manage.py
|   `-- myproject
|       |-- __init__.py
|       |-- settings.py
|       |-- urls.py
|       `-- wsgi.py
|-- README.md
`-- requirements.txt
```

Continuing ...

```
cd myproject/
sed -i 's/^ALLOWED_HOSTS/# ALLOWED_HOSTS/' myproject/settings.py
echo 'ALLOWED_HOSTS = ["*"]' >> myproject/settings.py
python manage.py runserver 0.0.0.0:8888

# View in web browser or
curl -s http://0.0.0.0:8888 |egrep 'It worked'
  <h1>It worked!</h1>
```

Create superuser

```
python manage.py migrate
python manage.py createsuperuser 
python manage.py runserver 0.0.0.0:8888

# Now view in web browser /admin/
# And make another user, if you want to dive into the 2nd user you can
# make this second user staff or superuser or ...

```
