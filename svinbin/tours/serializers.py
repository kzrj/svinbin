# -*- coding: utf-8 -*-
from rest_framework import serializers

from tours.models import Tour, MetaTour

from sows_events.serializers import SimpleSeminationSerializer, SimpleUltrasoundSerializer, \
    SimpleSowFarrowSerializer, SimpleWeaningSowSerializer


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'


class SowCycleSerializer(serializers.ModelSerializer):
    sow_semination = SimpleSeminationSerializer(many=True)
    sow_ultrasound = SimpleUltrasoundSerializer(many=True)
    sow_farrow = SimpleSowFarrowSerializer(many=True)
    sow_weaning = SimpleWeaningSowSerializer(many=True)

    class Meta:
        model = Tour
        fields = ['week_number', 'year', 'sow_semination', 'sow_ultrasound', 'sow_farrow', 'sow_weaning']