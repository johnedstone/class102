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
