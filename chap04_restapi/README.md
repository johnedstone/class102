### Errata
* Note: Somehow `django-rest-framework==0.1.0` crept into the requirements file.
This can safely be deleted.

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

### Quick curl example
Curl example
```

curl -vs --header 'Content-Type: application/json' --header 'Accept: application/json' --header 'Authorization: Token aaae533453898571503363346eda985e709b080b' -d '{"bucket":"johnedstone-Oct-04-01", "change":"change", "dry_run": false}' http://127.0.0.1:8000/api/create-bucket/ | python -m json.tool

{
    "bucket": "johnedstone-Oct-04-01",
    "bucket_creation_date": "2017-10-04 11:58:05-04:00",
    "change": "change",
    "client_id_display": "boohoo",
    "dry_run": false,
    "http_status_code": 200,
    "location": "",
    "new_bucket": "no",
    "request_created": "2017-10-04T16:00:51.526802Z",
    "s3_error": "",
    "status": "Bucket already exists",
    "url": "http://127.0.0.1:8000/api/create-bucket/29/"
}

```

Which is equivilant to python's HTTPie

```
http http://127.0.0.1:8000/api/create-bucket/ "Authorization: Token aaae533453898571503363346eda985e709b080b" bucket="johnedstone-Oct-04-01" change="change" dry_run=false
HTTP/1.0 201 Created
Allow: GET, HEAD, OPTIONS, POST
Content-Length: 350
Content-Type: application/json
Date: Wed, 04 Oct 2017 16:04:55 GMT
Location: http://127.0.0.1:8000/api/create-bucket/30/
Server: WSGIServer/0.2 CPython/3.5.1
X-Frame-Options: SAMEORIGIN

{
    "bucket": "johnedstone-Oct-04-01",
    "bucket_creation_date": "2017-10-04 11:58:05-04:00",
    "change": "change",
    "client_id_display": "boohoo",
    "dry_run": false,
    "http_status_code": 200,
    "location": "",
    "new_bucket": "no",
    "request_created": "2017-10-04T16:04:55.824678Z",
    "s3_error": "",
    "status": "Bucket already exists",
    "url": "http://127.0.0.1:8000/api/create-bucket/30/"
}

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

### REST API: doing a task, v0.9
```
pip install --proxy ${PIP_PROXY} boto3
pip freeze | egrep -i 'boto3' >> requirements.txt
```
* update aws_bucket_app/{serializers,urls,viewsets,models}.py, restapi_project/settings.py
* update environmental variables

```
python manage.py makemigrations
python manage.py migrate

source aws_keys.sh
python manage.py runserver

# Test the endpoint

http http://127.0.0.1:8000/api/create-bucket/ "Authorization: Token c39ada004cb0f930df0ba6ca380c9485e9207913" bucket=johnedstone-holy-cow-1234 change=ABC1234567
HTTP/1.0 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 334
Content-Type: application/json
Date: Fri, 29 Sep 2017 07:18:53 GMT
Location: http://127.0.0.1:8000/api/create-bucket/3/

{
    "bucket": "johnedstone-holy-cow-1234",
    "change": "ABC1234567",
    "created": "2017-09-29T07:18:53.793051Z",
    "http_status_code": 99,
    "location": "",
    "modified": "2017-09-29T07:18:53.793145Z",
    "s3_error": "('Connection aborted.', ConnectionRefusedError(111, 'Connection refused'))",
    "status": "Failed",
    "url": "http://127.0.0.1:8000/api/create-bucket/3/"
}

http http://127.0.0.1:8000/api/create-bucket/ "Authorization: Token c39ada004cb0f930df0ba6ca380c9485e9207913"
HTTP/1.0 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 995
Content-Type: application/json
Date: Fri, 29 Sep 2017 07:21:56 GMT
Server: WSGIServer/0.2 CPython/3.5.1
X-Frame-Options: SAMEORIGIN

[
    {
        "bucket": "johnedstone-holy-cow",
        "change": "ABC123",
        "created": "2017-09-29T07:14:22.585989Z",
        "http_status_code": 99,
        "location": "",
        "modified": "2017-09-29T07:14:22.586089Z",
        "s3_error": "('Connection aborted.', ConnectionRefusedError(111, 'Connection refused'))",
        "status": "Failed",
        "url": "http://127.0.0.1:8000/api/create-bucket/1/"
    },
    {
        "bucket": "johnedstone-holy-cow-123",
        "change": "ABC123456",
        "created": "2017-09-29T07:17:04.612530Z",
        "http_status_code": 99,
        "location": "",
        "modified": "2017-09-29T07:17:04.612616Z",
        "s3_error": "('Connection aborted.', ConnectionRefusedError(111, 'Connection refused'))",
        "status": "Failed",
        "url": "http://127.0.0.1:8000/api/create-bucket/2/"
    },
    {
        "bucket": "johnedstone-holy-cow-1234",
        "change": "ABC1234567",
        "created": "2017-09-29T07:18:53.793051Z",
        "http_status_code": 99,
        "location": "",
        "modified": "2017-09-29T07:18:53.793145Z",
        "s3_error": "('Connection aborted.', ConnectionRefusedError(111, 'Connection refused'))",
        "status": "Failed",
        "url": "http://127.0.0.1:8000/api/create-bucket/3/"
    }
]


```
### Tag v0.10
* Fix proxy
* Fix validation, and remove unique contraint on bucket and change
* REMEMBER to run MAKEMIGRATIONS and MIGRATE
* Looks like AWS _doesnt' throw and error_ if the bucket is already present
```
source ~/.virtualenvs/class102_chap04/bin/activate
export LD_LIBRARY_PATH=/opt/rh/rh-python35/root/usr/lib64
cd class102/chap04_restapi/restapi_project/
source aws_keys.sh

python manage.py shell
>>> from aws_bucket_app.models import CreateBucket as CB
>>> cb = CB()
>>> cb.bucket = 'johnedstone-27-Sep'
>>> cb.change = 'MyChange'
>>> cb.full_clean()
>>> cb.save()
INFO:bucket:37:Bucket:johnedstone-27-Sep, AK: some-access-key
>>> cb.status
'Success'
>>> cb.http_status_code
200
>>> cb.response_string
"{'ResponseMetadata': {'RetryAttempts': 0, 'HTTPHeaders': {'server': 'AmazonS3', 'x-amz-id-2': 'H9WMtAbM9FEMPZclz2OJ8yj92yN9p7fjpXLBf3506Mudl+f+GTiXJD7S/IaGRwY3AXNN9Zaf5sI=', 'date': 'Sat, 30 Sep 2017 02:58:42 GMT', 'location': '/johnedstone-27-Sep', 'x-amz-request-id': '89698527217D91DD', 'content-length': '0'}, 'HostId': 'H9WMtAbM9FEMPZclz2OJ8yj92yN9p7fjpXLBf3506Mudl+f+GTiXJD7S/IaGRwY3AXNN9Zaf5sI=', 'RequestId': '89698527217D91DD', 'HTTPStatusCode': 200}, 'Location': '/johnedstone-27-Sep'}"
>>>
>>> cb_02 = CB()
>>> cb_02.bucket = 'johnedstone-27-Sep'
>>> cb_02.change = 'MyChange'
>>> cb_02.full_clean()
>>> cb_02.save()
INFO:bucket:37:Bucket:johnedstone-27-Sep, AK: some-access-key
>>> cb_02.status
'Success'
>>> cb_02.http_status_code
200
>>> cb_02.response_string
"{'ResponseMetadata': {'RetryAttempts': 0, 'HTTPHeaders': {'server': 'AmazonS3', 'x-amz-id-2': 'cHDi3MM9IwlKuQUbkXinOpNkMQVwjtsb43IX4rKwjFNoiAKkhId3jBxWjZbiNbeWu+C+7Mt6ww4=', 'date': 'Sat, 30 Sep 2017 03:00:12 GMT', 'location': '/johnedstone-27-Sep', 'x-amz-request-id': 'F34D3D167408DD26', 'content-length': '0'}, 'HostId': 'cHDi3MM9IwlKuQUbkXinOpNkMQVwjtsb43IX4rKwjFNoiAKkhId3jBxWjZbiNbeWu+C+7Mt6ww4=', 'RequestId': 'F34D3D167408DD26', 'HTTPStatusCode': 200}, 'Location': '/johnedstone-27-Sep'}"
```

### Tag v0.11 Swagger
* https://django-rest-swagger.readthedocs.io/en/latest/
```
pwd
# Output: class102/chap04_restapi/restapi_project

pip install --proxy $PIP_PROXY django-rest-swagger
pip freeze | egrep -i swagger | tee -a requirements.txt
```

* Add 'rest_framework_swagger' to INSTALLED_APPS in Django settings.
* Update `restapi_project/urls.py` and other files (see below) to tab v0.11 then runserver and visit to `/swagger`
```
#       modified:   aws_bucket_app/views.py
#       modified:   requirements.txt
#       modified:   restapi_project/settings.py
#       modified:   restapi_project/urls.py
```

### Tag v0.12 Using Token authentication, and
* Added `dry-run` and `user` field to Create Bucket
* The following files were updated
* The db and the migration files were deleted and `makemigration` and `migrate` were run again
```
#       modified:   aws_bucket_app/models.py
#       modified:   aws_bucket_app/serializers.py
#       modified:   aws_bucket_app/views.py
#       modified:   aws_keys_openshift.parm
#       modified:   requirements.txt
#       modified:   restapi_project/settings.py
```

### Tag v0.13 Changing language to 
* Changing language fromu "username" to "Client ID" - remember to delete db and run `makemigrations`, `migrate`
* Moved create overide to a more rational place, `preform_create`
* files changed:
```
#       modified:   aws_bucket_app/models.py
#       modified:   aws_bucket_app/serializers.py
#       modified:   aws_bucket_app/views.py
#       modified:   aws_keys_openshift.parm
```

### Tag v0.14 Reporting back if bucket is pre-existing
* Create logic to catch _pre-existing_ bucket
* The following files were updated
* Run `makemigration` and `migrate`
```
#       modified:   aws_bucket_app/bucket.py
#       modified:   aws_bucket_app/models.py
#       modified:   aws_bucket_app/serializers.py
#       modified:   aws_bucket_app/views.py

```

### Tag v0.15
* Changes: adjusted logging so it can be 'turned on' in Openshift by env var
* Catching 'existing bucket' a little more clearly
* Adjust bucket success messaging so that it can be controlled from Openshift env var
* reduced output for user (now look in logging if more info is needed)
* update modified files, then

```
rm db.sqlite3
rm aws_bucket_app/migrations/000xxxx
python manage.py makemigrations
python manage.py migrate
```

* files changed:
```
#       modified:   aws_bucket_app/bucket.py
#       modified:   aws_bucket_app/models.py
#       modified:   aws_bucket_app/serializers.py
#       modified:   aws_bucket_app/views.py
#       modified:   restapi_project/settings.py
#       modified:   typical_aws_keys.sh
#       modified:   typical_aws_keys_openshift.parm
```

### Tag v0.16
* Write management tool for setting token
* Write Openshift template and deploy
* Added whitenoise so that swagger can be viewed in Openshift - see `requirements.txt` and `settings.py`
* Added several env variables
* Files changed between tag v0.15 and v0.16
```
chap04_restapi/README.md
chap04_restapi/restapi_project/.s2i/bin/run
chap04_restapi/restapi_project/aws_bucket_app/bucket.py
chap04_restapi/restapi_project/aws_bucket_app/management/__init__.py
chap04_restapi/restapi_project/aws_bucket_app/management/commands/__init__.py
chap04_restapi/restapi_project/aws_bucket_app/management/commands/set_client_token.py
chap04_restapi/restapi_project/aws_bucket_app/migrations/0001_initial.py
chap04_restapi/restapi_project/aws_bucket_app/models.py
chap04_restapi/restapi_project/openshift/templates/non_prod_sqlite3.yaml
chap04_restapi/restapi_project/openshift/templates/prod_sqlite3.yaml
chap04_restapi/restapi_project/requirements.txt
chap04_restapi/restapi_project/restapi_project/settings.py
chap04_restapi/restapi_project/typical_aws_keys.sh
chap04_restapi/restapi_project/typical_aws_keys_openshift.parm
```

#### Deploy in Openshift
* First ...
```
oc new-project project-name
oc secrets new-sshauth sshsecret --ssh-privatekey=/path/to/key/
oc secret add serviceaccount/builder secrets/sshsecret
```

* Building ...
```
oc new-app --param-file aws_keys_openshift.parm -f openshift/templates/non_prod_sqlite3.yaml
```

* Or just deploying ...
```
oc new-app --param-file aws_keys_openshift.parm -f openshift/templates/prod_sqlite3.yaml
```

# Next
* Start Chapter 5
* start using postgresql json field, so that a dictionary of tags can be used

### To Do:
* Consider using AWS Lambda
