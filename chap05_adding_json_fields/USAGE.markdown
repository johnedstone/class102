#### Usage
* Showing both curl and the python client, [HTTPie](https://httpie.org/)
* Currently, only creating S3 Buckets is supported.  Updating and deleting may be supported at later date.
* The superuser can list all the requests in the ephemeral database.  Each use can only view their requests.

#### Simple case, following the endpoint, 302 Status code

```
curl -s --header 'Content-Type: application/json' --header 'Accept: application/json' https://yourserver.com/

curl -s -I --header 'Content-Type: application/json' --header 'Accept: application/json' https://yourserver.com/
HTTP/1.1 302 Found
Server: gunicorn/19.7.1
Date: Wed, 11 Oct 2017 15:13:17 GMT
X-Frame-Options: SAMEORIGIN
Content-Type: text/html; charset=utf-8
Content-Length: 0
Location: /api/

http https://yourserver.com/
HTTP/1.1 302 Found
Content-Length: 0
Content-Type: text/html; charset=utf-8
Date: Wed, 11 Oct 2017 15:13:59 GMT
Location: /api/
Server: gunicorn/19.7.1

#### Following
curl -s --header 'Content-Type: application/json' --header 'Accept: application/json' https://yourserver.com/api/ | python -m json.tool
{
    "s3-bucket": "https://yourserver.com/api/s3-bucket/"
}

curl -s -I --header 'Content-Type: application/json' --header 'Accept: application/json' https://yourserver.com/api/
HTTP/1.1 200 OK
Server: gunicorn/19.7.1
Date: Wed, 11 Oct 2017 15:28:33 GMT
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Content-Length: 84
Allow: GET, HEAD, OPTIONS

http https://yourserver.com/api/
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Cache-control: private
Content-Length: 84
Content-Type: application/json
Date: Wed, 11 Oct 2017 15:28:44 GMT
Server: gunicorn/19.7.1

{
    "s3-bucket": "https://yourserver.com/api/s3-bucket/"
}

```

#### Is CORS enabled? Yes
Notice: `Access-Control-Allow-Origin: *`
```
curl -s -I --header 'Origin: http://boo.hoo.com/' --header 'Content-Type: application/json' --header 'Accept: application/json' https://yourserver.com/api/
HTTP/1.1 200 OK
Server: gunicorn/19.7.1
Date: Wed, 11 Oct 2017 15:32:26 GMT
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Content-Length: 84
Allow: GET, HEAD, OPTIONS
Access-Control-Allow-Origin: *

http https://yourserver.com/api/ "Origin: http://boo.hoo.com/"
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Allow: GET, HEAD, OPTIONS
Content-Length: 84
Content-Type: application/json
Date: Wed, 11 Oct 2017 15:31:54 GMT
Server: gunicorn/19.7.1

{
    "s3-bucket": "https://yourserver.com/api/s3-bucket/"
}

```

#### Simplest S3 request
Taking all the defaults, first dry_run=false (default), then setting dry_run=false

```
curl -sv -d '{"bucket": "a.test.bucket.01", "change": "CHGxxxxx"}' --header 'Content-Type: application/json' --header 'Accept: application/json' --header 'Authorization: Token yourprivatetoken'  https://yourserver.com/api/s3-bucket/ | python -m json.tool

< HTTP/1.1 201 Created
< Server: gunicorn/19.7.1
< Date: Wed, 11 Oct 2017 15:48:31 GMT
< X-Frame-Options: SAMEORIGIN
< Content-Type: application/json
< Content-Length: 459
< Location: https://yourserver.com/api/s3-bucket/2/
< Allow: GET, HEAD, OPTIONS, POST
< Set-Cookie: e68308a4bbbe1525ae78812b994f396d=4670661caa25b6725805aa8129f85532; path=/; HttpOnly; Secure
<

{
    "acl": "public-read",
    "amz_bucket_region": "unknown",
    "bucket": "a.test.bucket.01",
    "bucket_creation_date": "",
    "change": "CHGxxxxx",
    "client_id_display": "boohoo",
    "dry_run": true,
    "http_status_code": "unknown",
    "location": "",
    "location_constraint": "",
    "new_bucket": "unknown",
    "request_created": "2017-10-11T15:48:31.627891Z",
    "s3_error": "",
    "status": "Dry Run",
    "tag_set_list": [],
    "tag_set_created": [],
    "url": "https://yourserver.com/api/s3-bucket/2/"
}

curl -sv -d '{"bucket": "a.test.bucket.01", "change": "CHGxxxxx", "dry_run": false}' --header 'Content-Type: application/json' --header 'Accept: application/json' --header 'Authorization: Token yourprivatetoken'  https://yourserver.com/api/s3-bucket/ | python -m json.tool

< HTTP/1.1 201 Created
< Server: gunicorn/19.7.1
< Date: Wed, 11 Oct 2017 15:49:01 GMT
< X-Frame-Options: SAMEORIGIN
< Content-Type: application/json
< Content-Length: 507
< Location: https://yourserver.com/api/s3-bucket/3/
< Allow: GET, HEAD, OPTIONS, POST

{
    "acl": "public-read",
    "amz_bucket_region": "us-east-1",
    "bucket": "a.test.bucket.01",
    "bucket_creation_date": "2017-10-11 11:49:01-04:00",
    "change": "CHGxxxxx",
    "client_id_display": "boohoo",
    "dry_run": false,
    "http_status_code": "200",
    "location": "/a.test.bucket.01",
    "location_constraint": "",
    "new_bucket": "yes",
    "request_created": "2017-10-11T15:49:01.111893Z",
    "s3_error": "",
    "status": "New bucket created",
    "tag_set_list": [],
    "tag_set_created": [],
    "url": "https://yourserver.com/api/s3-bucket/3/"
}

http https://yourserver.com/api/s3-bucket/ "Authorization: Token yourprivatetoken" bucket=a.test.bucket.02 change=CHGxxx
HTTP/1.1 201 Created
Allow: GET, HEAD, OPTIONS, POST
Content-Length: 457
Content-Type: application/json
Date: Wed, 11 Oct 2017 15:50:20 GMT
Location: https://yourserver.com/api/s3-bucket/4/
Server: gunicorn/19.7.1
{
    "acl": "public-read",
    "amz_bucket_region": "unknown",
    "bucket": "a.test.bucket.02",
    "bucket_creation_date": "",
    "change": "CHGxxx",
    "client_id_display": "boohoo",
    "dry_run": true,
    "http_status_code": "unknown",
    "location": "",
    "location_constraint": "",
    "new_bucket": "unknown",
    "request_created": "2017-10-11T15:50:20.087831Z",
    "s3_error": "",
    "status": "Dry Run",
    "tag_set_created": [],
    "tag_set_list": [],
    "url": "https://yourserver.com/api/s3-bucket/4/"
}

http https://yourserver.com/api/s3-bucket/ "Authorization: Token yourprivatetoken" bucket=a.test.bucket.02 change=CHGxxx dry_run=false
HTTP/1.1 201 Created
Allow: GET, HEAD, OPTIONS, POST
Content-Length: 505
Content-Type: application/json
Date: Wed, 11 Oct 2017 15:50:44 GMT
Location: https://yourserver.com/api/s3-bucket/5/
Server: gunicorn/19.7.1
{
    "acl": "public-read",
    "amz_bucket_region": "us-east-1",
    "bucket": "a.test.bucket.02",
    "bucket_creation_date": "2017-10-11 11:50:44-04:00",
    "change": "CHGxxx",
    "client_id_display": "boohoo",
    "dry_run": false,
    "http_status_code": "200",
    "location": "/a.test.bucket.02",
    "location_constraint": "",
    "new_bucket": "yes",
    "request_created": "2017-10-11T15:50:44.251244Z",
    "s3_error": "",
    "status": "New bucket created",
    "tag_set_created": [],
    "tag_set_list": [],
    "url": "https://yourserver.com/api/s3-bucket/5/"
}


```

#### Using the field `tag_set_list` showing validation error as well
For example, if the tags were needed "System Owner" and "Charge Center"
```
https://yourserver.com/api/s3-bucket/ "Authorization: Token yourprivatetoken" bucket=a.test.bucket.03 change=CHGxxx dry_run=false tag_set_list:='{"System Owner": "Charlie Brown", "Charge Center": "Lucy"}'
HTTP/1.1 400 Bad Request

{
    "tag_set_list": [
        "tag_set_list, {'System Owner': 'Charlie Brown', 'Charge Center': 'Lucy'}, is not a list, e.g. [{\"key\": \"value\"},]"
    ]
}

http https://yourserver.com/api/s3-bucket/ "Authorization: Token yourprivatetoken" bucket=a.test.bucket.03 change=CHGxxx dry_run=false tag_set_list:='[{"System Owner": "Charlie Brown"}, {"Charge Center": "Lucy"}]'
HTTP/1.1 201 Created
Allow: GET, HEAD, OPTIONS, POST
Content-Length: 647
Content-Type: application/json
Date: Wed, 11 Oct 2017 17:26:26 GMT
Location: https://yourserver.com/api/s3-bucket/7/
Server: gunicorn/19.7.1

{
    "acl": "public-read",
    "amz_bucket_region": "us-east-1",
    "bucket": "a.test.bucket.03",
    "bucket_creation_date": "2017-10-11 13:26:27-04:00",
    "change": "CHGxxx",
    "client_id_display": "boohoo",
    "dry_run": false,
    "http_status_code": "200",
    "location": "/a.test.bucket.03",
    "location_constraint": "",
    "new_bucket": "yes",
    "request_created": "2017-10-11T17:26:26.862528Z",
    "s3_error": "",
    "status": "New bucket created",
    "tag_set_created": [
        {
            "Key": "Charge Center",
            "Value": "Lucy"
        },
        {
            "Key": "System Owner",
            "Value": "Charlie Brown"
        }
    ],
    "tag_set_list": [
        {
            "System Owner": "Charlie Brown"
        },
        {
            "Charge Center": "Lucy"
        }
    ],
    "url": "https://yourserver.com/api/s3-bucket/7/"
}

curl -sv -d '{"bucket": "a.test.bucket.06", "change": "CHGxxxxx", "dry_run": false, "tag_set_list": [{"System Owner": "Charlie Brown"}, {"Charge Center": "Lucy"}]}' --header 'Content-Type: application/json' --header 'Accept: application/json' --header 'Authorization: Token yourprivatetoken'  https://yourserver.com/api/s3-bucket/ | python -m json.tool
< HTTP/1.1 201 Created
< Server: gunicorn/19.7.1
< Date: Wed, 11 Oct 2017 17:35:43 GMT
< X-Frame-Options: SAMEORIGIN
< Content-Type: application/json
< Content-Length: 650
< Location: https://yourserver.com/api/s3-bucket/10/
< Allow: GET, HEAD, OPTIONS, POST
<
{
    "acl": "public-read",
    "amz_bucket_region": "us-east-1",
    "bucket": "a.test.bucket.06",
    "bucket_creation_date": "2017-10-11 13:35:43-04:00",
    "change": "CHGxxxxx",
    "client_id_display": "boohoo",
    "dry_run": false,
    "http_status_code": "200",
    "location": "/a.test.bucket.06",
    "location_constraint": "",
    "new_bucket": "yes",
    "request_created": "2017-10-11T17:35:43.256556Z",
    "s3_error": "",
    "status": "New bucket created",
    "tag_set_list": [
        {
            "System Owner": "Charlie Brown"
        },
        {
            "Charge Center": "Lucy"
        }
    ],
    "tag_set_created": [
        {
            "Key": "Charge Center",
            "Value": "Lucy"
        },
        {
            "Key": "System Owner",
            "Value": "Charlie Brown"
        }
    ],
    "url": "https://yourserver.com/api/s3-bucket/10/"
}

```

#### Just in case: gettting your token, if you forgot
```
http https://yourserver.com/api-token-auth/ username=your-client-id password=your-password
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Content-Length: 32
Content-Type: application/json
Date: Wed, 11 Oct 2017 15:46:38 GMT
Server: gunicorn/19.7.1

{
    "token": "yourprivatetoken"
}
```

#### Using the OPTIONS method to list the available fields: `read_only: false`

Note:
* More fields may be added, use this as an example only
* An Authorization Token is not needed

```
curl -sv -X OPTIONS --header 'Content-Type: application/json' --header 'Accept: application/json'  https://yourserver.com/api/s3-bucket/ | python -m json.tool 
> OPTIONS /api/s3-bucket/ HTTP/1.1
> User-Agent: curl/7.29.0
> Host: yourserver.com
> Content-Type: application/json
> Accept: application/json
>
< HTTP/1.1 200 OK
< Server: gunicorn/19.7.1
< Date: Wed, 11 Oct 2017 16:01:23 GMT
< X-Frame-Options: SAMEORIGIN
< Content-Type: application/json
< Content-Length: 2546
< Allow: GET, HEAD, OPTIONS, POST

{
    "name": "S3 Bucket List",
    "description": "",
    "renders": [
        "application/json"
    ],
    "parses": [
        "application/json",
        "application/x-www-form-urlencoded",
        "multipart/form-data"
    ],
    "actions": {
        "POST": {
            "acl": {
                "type": "choice",
                "required": false,
                "read_only": false,
                "label": "Acl",
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
                ]
            },
            "amz_bucket_region": {
                "type": "field",
                "required": false,
                "read_only": true,
                "label": "Amz bucket region"
            },
            "bucket": {
                "type": "string",
                "required": true,
                "read_only": false,
                "label": "Bucket",
                "min_length": 3,
                "max_length": 63
            },
            "bucket_creation_date": {
                "type": "string",
                "required": false,
                "read_only": true,
                "label": "Bucket creation date"
            },
            "change": {
                "type": "string",
                "required": true,
                "read_only": false,
                "label": "Change",
                "max_length": 25
            },
            "client_id_display": {
                "type": "field",
                "required": false,
                "read_only": true,
                "label": "Client id display"
            },
            "dry_run": {
                "type": "boolean",
                "required": false,
                "read_only": false,
                "label": "Dry run"
            },
            "http_status_code": {
                "type": "field",
                "required": false,
                "read_only": true,
                "label": "Http status code"
            },
            "location": {
                "type": "field",
                "required": false,
                "read_only": true,
                "label": "Location"
            },
            "location_constraint": {
                "type": "choice",
                "required": false,
                "read_only": false,
                "label": "Location constraint",
                "choices": [
                    {
                        "display_name": "EU",
                        "value": "EU"
                    },
                    {
                        "display_name": "eu-west-1",
                        "value": "eu-west-1"
                    },
                    {
                        "display_name": "us-west-1",
                        "value": "us-west-1"
                    },
                    {
                        "display_name": "us-west-2",
                        "value": "us-west-2"
                    },
                    {
                        "display_name": "ap-south-1",
                        "value": "ap-south-1"
                    },
                    {
                        "display_name": "ap-southeast-1",
                        "value": "ap-southeast-1"
                    },
                    {
                        "display_name": "ap-southeast-2",
                        "value": "ap-southeast-2"
                    },
                    {
                        "display_name": "ap-northeast-1",
                        "value": "ap-northeast-1"
                    },
                    {
                        "display_name": "sa-east-1",
                        "value": "sa-east-1"
                    },
                    {
                        "display_name": "cn-north-1",
                        "value": "cn-north-1"
                    },
                    {
                        "display_name": "eu-central-1",
                        "value": "eu-central-1"
                    }
                ]
            },
            "new_bucket": {
                "type": "string",
                "required": false,
                "read_only": true,
                "label": "New bucket"
            },
            "request_created": {
                "type": "datetime",
                "required": false,
                "read_only": true,
                "label": "Request created"
            },
            "s3_error": {
                "type": "string",
                "required": false,
                "read_only": true,
                "label": "S3 error"
            },
            "status": {
                "type": "string",
                "required": false,
                "read_only": true,
                "label": "Status"
            },
            "tag_set_list": {
                "type": "field",
                "required": false,
                "read_only": false,
                "label": "Tag set list"
            },
            "tag_set_created": {
                "type": "field",
                "required": false,
                "read_only": true,
                "label": "Tag set created"
            },
            "url": {
                "type": "field",
                "required": false,
                "read_only": true,
                "label": "Url"
            }
        }
    }
}

#### Or with HTTPie
http OPTIONS https://yourserver.com/api/s3-bucket/
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS, POST
Cache-control: private
Content-Length: 2546
Content-Type: application/json
Date: Wed, 11 Oct 2017 17:20:28 GMT
Server: gunicorn/19.7.1

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
.....
```
