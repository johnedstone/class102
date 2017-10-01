# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, permissions

from .models import RainbowColor, DogBreed, CreateBucket
from .serializers import (RainbowColorSerializer,
    DogBreedSerializer, CreateBucketSerializer)


class RainbowColorViewSet(viewsets.ModelViewSet):
    queryset = RainbowColor.objects.all()
    serializer_class = RainbowColorSerializer
    http_method_names = ['get', 'head', 'options', 'post']

class DogBreedViewSet(viewsets.ModelViewSet):
    queryset = DogBreed.objects.all()
    serializer_class = DogBreedSerializer
    http_method_names = ['get', 'head', 'options', 'post']
    # permission_classes = (permissions.IsAuthenticated,)

class CreateBucketViewSet(viewsets.ModelViewSet):
    queryset = CreateBucket.objects.all()
    serializer_class = CreateBucketSerializer
    http_method_names = ['get', 'head', 'options', 'post']
    # permission_classes = (permissions.IsAuthenticated,)


# vim: ai et ts=4 sw=4 sts=4 ru nu
