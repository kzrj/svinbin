# # -*- coding: utf-8 -*-
from rest_framework import serializers

from piglets_events.models import CullingPiglets, WeighingPiglets, Recount
from locations.models import Location


class CullingPigletsSerializer(serializers.ModelSerializer):
    date = serializers.CharField(default=None, allow_blank=True)
    quantity = serializers.IntegerField(default=1)
    total_weight = serializers.FloatField(required=False)

    class Meta:
        model = CullingPiglets
        fields = ['culling_type', 'reason', 'quantity', 'date',
            'total_weight', 'piglets_age']


class CullingPigletsReadSerializer(serializers.ModelSerializer):
    average_weight = serializers.ReadOnlyField()
    date = serializers.DateTimeField(format='%d-%m-%Y')

    class Meta:
        model = CullingPiglets
        fields = ['culling_type', 'reason', 'quantity', 'date',
            'total_weight', 'piglets_age', 'average_weight']


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


class WeighingPigletsReadSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format='%d-%m-%Y')
    average_weight = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = WeighingPiglets
        fields = ['date', 'total_weight', 'average_weight', 'piglets_quantity', 'piglets_age']


class RecountWeighingPigletsSerializer(serializers.ModelSerializer):
    new_quantity = serializers.IntegerField(required=False)

    class Meta:
        model = WeighingPiglets
        fields = ['total_weight', 'place', 'new_quantity']


class RecountPigletsSerializer(serializers.Serializer):
    new_quantity = serializers.IntegerField()
    comment = serializers.CharField(required=False)
