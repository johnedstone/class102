from rest_framework import routers

from .views import (
    CreateBucketViewSet,
    )

router = routers.DefaultRouter()
# no name/namespace here
router.register(r's3-bucket', CreateBucketViewSet)

# vim: ai et ts=4 sts=4 sw=4 ru nu
