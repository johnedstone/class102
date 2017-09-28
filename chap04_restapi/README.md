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

