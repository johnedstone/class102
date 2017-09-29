from rest_framework import routers

from .views import (
    RainbowColorViewSet,
    DogBreedViewSet,
    CreateBucketViewSet,
    )

router = routers.DefaultRouter()
# no name/namespace here
router.register(r'rainbow-color', RainbowColorViewSet)
router.register(r'dog-breed', DogBreedViewSet)
router.register(r'create-bucket', CreateBucketViewSet)

# vim: ai et ts=4 sts=4 sw=4 ru nu
