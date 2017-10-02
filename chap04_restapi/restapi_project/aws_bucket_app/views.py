# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated

from .models import RainbowColor, DogBreed, CreateBucket
from .serializers import (RainbowColorSerializer,
    DogBreedSerializer, CreateBucketSerializer)

logger = logging.getLogger('verbose_logging')

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

    def list(self, request, *args, **kwargs):

        # Putting this check here not in permission_classes
        # so that Swagger will show List
        if not request.user.is_authenticated:
            raise NotAuthenticated

        # http://www.cdrf.co/3.6/rest_framework.viewsets/ModelViewSet.html
        queryset = self.filter_queryset(self.get_queryset()).filter(client=request.user)

        if request.user.is_superuser:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """ http://www.django-rest-framework.org/topics/3.0-announcement/
            http://www.cdrf.co/3.6/rest_framework.viewsets/ModelViewSet.html
        """

        serializer.save(client=self.request.user)

# vim: ai et ts=4 sw=4 sts=4 ru nu
