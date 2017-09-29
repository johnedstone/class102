### Quick review

Note: using python HTTPie instead of curl

* simplest case: model, viewset, serializer
```
http GET https://promotion-restapi.fqdn/api/environments/

# View: https://..._PaaS_Self ..../blob/master/rest_api/ocp_bkend_api/ocp_bkend_api_project/ocp_bkend_api/views.py

```

* more complex: overriding GET and LIST see [http://www.cdrf.co/3.6/rest_framework.viewsets/ModelViewSet.html](http://www.cdrf.co/3.6/rest_framework.viewsets/ModelViewSet.html), but keep it simple when you can

* and authorization

```
http https://promotion-restapi.fqdn/api-token-auth/ username=username password=password
# Returns Token
http  https://promotion-restapi.fqdn/api/deployconfigs/ "Authorization: Token <token>"
http  https://promotion-restapi.fqdn/api/promotions/ "Authorization: Token <token>"
```

### References
* http://www.django-rest-framework.org/
* http://www.cdrf.co/
### Let's get started - getting python 3.5 virtualenv on Centos/RH v0.6
Setting up, again, independent of previous chapters

```
pwd
class102

cd chap04_restapi/
scl enable rh-python35 bash
virtualenv-3.5 ~/.virtualenvs/class102_chap04
env |egrep LD

# Output ..
LD_LIBRARY_PATH=/opt/rh/rh-python35/root/usr/lib64

exit

pwd
class102/chap04_restapi

```

### Install package dependencies v0.6 - moving beyond, now, outside SCL

```
source ~/.virtualenvs/class102_chap04/bin/activate
export LD_LIBRARY_PATH=/opt/rh/rh-python35/root/usr/lib64
export PIP_PROXY=<ip:port>

pip install --proxy ${PIP_PROXY} pip --upgrade
pip install --proxy ${PIP_PROXY} django django-rest-framework django-cors-headers gunicorn httpie

pwd
class102/chap04_restapi

django-admin startproject restapi_project
cd restapi_project/

echo '# python 3.5.x' > requirements.txt
pip freeze | egrep -i 'django|rest|cores|http|gunicorn' >> requirements.txt

pwd
class102/chap04_restapi/restapi_project

django-admin startapp aws_bucket_app
pwd
class102/chap04_restapi/restapi_project

mv restapi_project/wsgi.py .

# Update restapi_project/{settings,urls}.py with v0.6

tree -I '*pyc'
.
|-- aws_bucket_app
|   |-- admin.py
|   |-- apps.py
|   |-- __init__.py
|   |-- migrations
|   |   |-- __init__.py
|   |   `-- __pycache__
|   |-- models.py
|   |-- __pycache__
|   |-- tests.py
|   `-- views.py
|-- db.sqlite3
|-- manage.py
|-- __pycache__
|-- requirements.txt
|-- restapi_project
|   |-- __init__.py
|   |-- __pycache__
|   |-- settings_orig.py
|   |-- settings.py
|   `-- urls.py
`-- wsgi.py

python manage.py migrate
python manage.py createsuperuser

python manage.py runserver

# Curl or use Httpie (http)
http http://127.0.0.1:8000/api-token-auth/ username=boohoo password=boohoowoohoo
HTTP/1.0 200 OK
Allow: POST, OPTIONS

{
    "token": "aebe186b17c7adc0a37be0222307f10fdf71b072"
}


```

### Setting up models v0.7

* Setup models
    * copy aws_bucket_app/{urls,models,serializers,views}.py
    * copy restapi_project/urls.py

```
python manage.py makemigrations
python manage.py migrate

# make users
python manage.py shell
>>> from django.contrib.auth.models import User
>>> u = User()
>>> u.username = 'userone'
>>> u.set_password('harrypotter')
>>> u.full_clean()
>>> u.save()
>>>

```

### Examples with models v0.7 using python HTTPie, not curl
```
http http://127.0.0.1:8000/
HTTP/1.0 302 Found
Location: /api/


http http://127.0.0.1:8000/api/
HTTP/1.0 200 OK
{
    "dog-breed": "http://127.0.0.1:8000/api/dog-breed/",
    "rainbow-color": "http://127.0.0.1:8000/api/rainbow-color/"
}

http http://127.0.0.1:8000/api/rainbow-color/ year_discovered='1911'
HTTP/1.0 400 Bad Request
{
    "color": [
        "This field is required."
    ]
}

http http://127.0.0.1:8000/api/rainbow-color/ color='yellow' year_discovered='1911'
HTTP/1.0 201 Created
Location: http://127.0.0.1:8000/api/rainbow-color/2/
{
    "color": "yellow",
    "fullname": "yellow:",
    "url": "http://127.0.0.1:8000/api/rainbow-color/2/"
}

http http://127.0.0.1:8000/api/rainbow-color/ color='yellow' year_discovered='1911'
HTTP/1.0 400 Bad Request
{
    "color": [
        "rainbow color with this color already exists."
    ]
}

http http://127.0.0.1:8000/api/rainbow-color/
HTTP/1.0 200 OK
[
    {
        "color": "blue",
        "fullname": "blue:1911",
        "url": "http://127.0.0.1:8000/api/rainbow-color/1/"
    },
    {
        "color": "yellow",
        "fullname": "yellow:",
        "url": "http://127.0.0.1:8000/api/rainbow-color/2/"
    }
]
```
### Examples with authenication v0.7 using python HTTPie, not curl
```
http http://127.0.0.1:8000/api-token-auth/ username=userone password=harrypotter
HTTP/1.0 200 OK
{
    "token": "c39ada004cb0f930df0ba6ca380c9485e9207913"
}

http http://127.0.0.1:8000/api/dog-breed/ "Authorization: Token c39ada004cb0f930df0ba6ca380c9485e9207913" breed='hotdog'
HTTP/1.0 400 Bad Request
{
    "year_discovered": [
        "This field is required."
    ]
}

http http://127.0.0.1:8000/api/dog-breed/ "Authorization: Token c39ada004cb0f930df0ba6ca380c9485e9207913" breed='hotdog' year_discovered='1011'
HTTP/1.0 201 Created
{
    "breed": "hotdog",
    "created": "2017-09-29T05:28:10.700482Z",
    "fullname": "hotdog:1011",
    "url": "http://127.0.0.1:8000/api/dog-breed/4/",
    "year_discovered": "1011"
}

http http://127.0.0.1:8000/api/dog-breed/4/ "Authorization: Token c39ada004cb0f930df0ba6ca380c9485e9207913"
HTTP/1.0 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 155
Content-Type: application/json
Date: Fri, 29 Sep 2017 05:28:37 GMT
Server: WSGIServer/0.2 CPython/3.5.1
X-Frame-Options: SAMEORIGIN
{
    "breed": "hotdog",
    "created": "2017-09-29T05:28:10.700482Z",
    "fullname": "hotdog:1011",
    "url": "http://127.0.0.1:8000/api/dog-breed/4/",
    "year_discovered": "1011"
}
```
