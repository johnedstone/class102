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
cd myproject/
django-admin startapp myapp
```

#### What is the current directory
At this point, the following commands will be executed from

```
pwd
class102/chap02_standard_django_hello_world/myproject
````



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

Add view and route
* Update myproject/settings.py per the diff below
* Update myproject/urls.py per the diff below
* Create myapp/urls.py as in this git repo
* Update myapp/views.py as in this git repo
* do `python manage.py runserver 0.0.0.0:8888`
* Next: Add models, and move on to the UI, then move on to REST API

```
git diff myproject/settings.py
@@ -37,6 +37,7 @@ INSTALLED_APPS = [
     'django.contrib.sessions',
     'django.contrib.messages',
     'django.contrib.staticfiles',
+    'myapp',
 ]

 MIDDLEWARE = [


git diff myproject/urls.py
@@ -13,9 +13,12 @@ Including another URLconf
     1. Import the include() function: from django.conf.urls import url, include
     2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
 """
-from django.conf.urls import url
+from django.conf.urls import url, include
 from django.contrib import admin
+from django.shortcuts import redirect

 urlpatterns = [
     url(r'^admin/', admin.site.urls),
+    url(r'^hello/', include('myapp.urls')),
+    url(r'^$', lambda x: redirect('/hello/', permanent=False)),
 ]

```
### References
* https://docs.djangoproject.com/en/1.11/intro/tutorial01/
