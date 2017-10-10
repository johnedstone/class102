from rest_framework import routers

from .views import (
    S3BucketViewSet,
    )

router = routers.DefaultRouter()
# no name/namespace here
router.register(r's3-bucket', S3BucketViewSet)

# vim: ai et ts=4 sts=4 sw=4 ru nu
