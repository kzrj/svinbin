# -*- coding: utf-8 -*-
from rest_framework import serializers

from tours.models import Tour


class TourSerializer(serializers.ModelSerializer):
    class Meta:
    	model = Tour
    	fields = '__all__'