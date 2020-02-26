# # -*- coding: utf-8 -*-
from rest_framework import serializers

from piglets_events.models import CullingPiglets, WeighingPiglets
from locations.models import Location


class CullingPigletsSerializer(serializers.ModelSerializer):
    is_it_gilt = serializers.BooleanField(default=False)

    class Meta:
        model = CullingPiglets
        fields = ['culling_type', 'reason', 'is_it_gilt']


class WeighingPigletsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeighingPiglets
        fields = ['total_weight', 'place',]


class WeighingReturnPigletsCreateSerializer(serializers.ModelSerializer):
    new_amount = serializers.IntegerField(required=False)
    to_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), required=False)

    class Meta:
        model = WeighingPiglets
        fields = ['total_weight', 'place', 'new_amount', 'to_location']


class WeighingPigletsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeighingPiglets
        fields = '__all__'


class RecountWeighingPigletsSerializer(serializers.ModelSerializer):
    new_quantity = serializers.IntegerField(required=False)

    class Meta:
        model = WeighingPiglets
        fields = ['total_weight', 'place', 'new_quantity']