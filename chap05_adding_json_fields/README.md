### Purpose
* Chapter 5 builds on the ideas presented in chapter 4, using PostgreSQL
* Add json fields to allow json dictionaries for tags by clients
* Start tagging at v5.01

### Tag v5.01
* Reduce models to just AWS S3 create bucket
* Create new templates with v5.xx tagging
* Added pip psycopg2
* change str(response)field to json
* Changed HTTP(S)_PROXY to AWS_HTTP(S)_Proxy 
* Added ACL and LocationConstraint
* Removed fields from model that can not be determined from s3_results JSONField

#### Files changed from Chap4 to Tag v5.01
```
chap03_models/chap3_project/chap3_app/templates/base.html

chap05_adding_json_fields/README.md
chap05_adding_json_fields/restapi_project/typical_aws_keys.sh
chap05_adding_json_fields/restapi_project/typical_aws_keys_openshift.parm
chap05_adding_json_fields/restapi_project/requirements.txt

chap05_adding_json_fields/restapi_project/aws_bucket_app/bucket.py
chap05_adding_json_fields/restapi_project/aws_bucket_app/migrations/0001_initial.py
chap05_adding_json_fields/restapi_project/aws_bucket_app/models.py
chap05_adding_json_fields/restapi_project/aws_bucket_app/serializers.py

chap05_adding_json_fields/restapi_project/restapi_project/settings.py
chap05_adding_json_fields/restapi_project/restapi_project/database.py

chap05_adding_json_fields/restapi_project/openshift/templates/django-psql-ephemeral.yaml
```

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
           -p POSTGRESQL_PASSWORD=${DATABASE_PASSWORD} \
           -p POSTGRESQL_DATABASE=${DATABASE_NAME} \
           -f openshift/templates/postgresql-ephemeral.yaml

# If HTTP(S)_PROXY is set, open another window to do port-forwarding
oc port-forward <pod> 5432

# In the original window and run these two commands
python manage.py migrate
python manage.py runserver
python manage.py set_client_token boohoo boohoowoohoo

# Then curl or httpie the API endpoint

# Cleaning up PostgreSQL project
oc delete all --all
oc delete secrets postgresql

# Examples using HTTPie
http http://127.0.0.1:8000/api/
http http://127.0.0.1:8000/api/create-bucket/ "Authorization: Token boohoowoohoo"

```

#### Notes on requesting the `OPTIONS` on an endpoint with HTTPie (or curl)

```
http OPTIONS http://127.0.0.1:8000/api/create-bucket/
[07/Oct/2017 22:49:55] "OPTIONS /api/create-bucket/ HTTP/1.1" 200 1573
HTTP/1.0 200 OK
Allow: GET, HEAD, OPTIONS, POST
Content-Length: 1573
Content-Type: application/json
Date: Sun, 08 Oct 2017 02:49:55 GMT
Server: WSGIServer/0.2 CPython/3.5.1
X-Frame-Options: SAMEORIGIN

{
    "actions": {
        "POST": {
            "acl": {
                "choices": [
                    {
                        "display_name": "private",
                        "value": "private"
                    },
                    {
                        "display_name": "public-read",
                        "value": "public-read"
                    },
                    {
                        "display_name": "public-read-write",
                        "value": "public-read-write"
                    },
                    {
                        "display_name": "authenticated-read",
                        "value": "authenticated-read"
                    }
                ],
                "label": "Acl",
                "read_only": false,
                "required": false,
                "type": "choice"
            },
            "bucket": {
                "label": "Bucket",
                "max_length": 255,
                "read_only": false,
                "required": true,
                "type": "string"
            },
            "bucket_creation_date": {
                "label": "Bucket creation date",
                "read_only": true,
                "required": false,
                "type": "string"
            },
            "change": {
                "label": "Change",
                "max_length": 25,
                "read_only": false,
                "required": true,
                "type": "string"
            },
            "client_id_display": {
                "label": "Client id display",
                "read_only": true,
                "required": false,
                "type": "field"
            },
            "dry_run": {
                "label": "Dry run",
                "read_only": false,
                "required": false,
                "type": "boolean"
...........
```

### Tag v5.02
* Added `@property` decorator back to model to be consistent, considering this as a property
* Add validator for S3 bucket naming
* Moved CHOICES on fields up to settings, so they can be controlled by os.getenv
* Files changed since v5.01
```
chap05_adding_json_fields/restapi_project/aws_bucket_app/bucket.py
chap05_adding_json_fields/restapi_project/aws_bucket_app/migrations/0001_initial.py
chap05_adding_json_fields/restapi_project/aws_bucket_app/models.py
chap05_adding_json_fields/restapi_project/restapi_project/settings.py
```


### Tag v5.03 in progress
* Add tagging http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.BucketTagging
* https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTtagging.html
* Files changed
```
chap05_adding_json_fields/restapi_project/aws_bucket_app/bucket.py
chap05_adding_json_fields/restapi_project/aws_bucket_app/migrations/0001_initial.py
chap05_adding_json_fields/restapi_project/aws_bucket_app/models.py
chap05_adding_json_fields/restapi_project/aws_bucket_app/serializers.py
chap05_adding_json_fields/restapi_project/restapi_project/settings.py
chap05_adding_json_fields/restapi_project/typical_aws_keys.sh
chap05_adding_json_fields/restapi_project/typical_aws_keys_openshift.parm
```

### Tag v5.04 next
* Added back CORS
* Changed endpoint from create-bucket to s3-bucket to be consistent with naming convention, removing the verb
* Fixed Location
* Changed model from CreateBucket to S3Bucket, again to be consistent with naming convention
* Update Openshift template, and default values

#### Example response
```
http http://127.0.0.1:8000/api/create-bucket/ "Authorization: Token boohoowoohoo" bucket="johnedstone-sat-15" change="CHXxxxx" dry_run=false location_constraint='us-west-1' acl='public-read'

HTTP/1.0 201 Created
Allow: GET, HEAD, OPTIONS, POST
Content-Length: 433
Content-Type: application/json
Date: Sun, 08 Oct 2017 05:36:16 GMT
Location: http://127.0.0.1:8000/api/create-bucket/2/
Server: WSGIServer/0.2 CPython/3.5.1
X-Frame-Options: SAMEORIGIN

{
    "acl": "public-read",
    "amz_bucket_region": "us-west-1",
    "bucket": "johnedstone-sat-15",
    "bucket_creation_date": "2017-10-08 01:36:15-04:00",
    "change": "CHXxxxx",
    "client_id_display": "boohoo",
    "dry_run": false,
    "http_status_code": "200",
    "location": "",
    "location_constraint": "us-west-1",
    "new_bucket": "yes",
    "request_created": "2017-10-08T05:36:16.044080Z",
    "s3_error": "",
    "status": "New bucket created",
    "url": "http://127.0.0.1:8000/api/create-bucket/2/"
```
