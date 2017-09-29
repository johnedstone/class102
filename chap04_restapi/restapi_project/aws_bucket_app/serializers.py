# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import RainbowColor, DogBreed

class RainbowColorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RainbowColor
        fields = ['url', 'color', 'fullname', 'created', 'year_discovered' ]
        required = ['color', 'year_discovered']
        read_only_fields = [field for field in fields if field not in ['color', 'year_discovered']]


class DogBreedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DogBreed
        fields = ['url', 'breed', 'fullname', 'created', 'year_discovered' ]
        read_only_fields = [field for field in fields if field not in ['breed', 'year_discovered']]
        required = ['breed', 'year_discovered']

# vim: ai et ts=4 sw=4 sts=4 ru nu 
