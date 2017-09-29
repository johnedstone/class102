from rest_framework import routers

from .views import RainbowColorViewSet, DogBreedViewSet

router = routers.DefaultRouter()
# no name/namespace here
router.register(r'rainbow-color', RainbowColorViewSet)
router.register(r'dog-breed', DogBreedViewSet)

# vim: ai et ts=4 sts=4 sw=4 ru nu
