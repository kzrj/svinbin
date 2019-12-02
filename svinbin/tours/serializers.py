# -*- coding: utf-8 -*-
from rest_framework import serializers

from tours.models import Tour, MetaTour


class TourSerializer(serializers.ModelSerializer):
    class Meta:
    	model = Tour
    	fields = '__all__'


class MetaTourSerializer(serializers.ModelSerializer):
    class Meta:
    	model = MetaTour
    	fields = '__all__'