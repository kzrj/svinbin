# # -*- coding: utf-8 -*-
from rest_framework import serializers

from piglets_events.models import CullingPiglets, WeighingPiglets
from locations.models import Location


class CullingPigletsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CullingPiglets
        fields = ['culling_type', 'reason']


class WeighingPigletsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeighingPiglets
        fields = ['total_weight', 'place',]


class WeighingReturnPigletsCreateSerializer(serializers.ModelSerializer):
    new_amount = serializers.IntegerField(required=False)
    to_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())

    class Meta:
        model = WeighingPiglets
        fields = ['total_weight', 'place', 'new_amount', 'to_location']


class WeighingPigletsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeighingPiglets
        fields = '__all__'