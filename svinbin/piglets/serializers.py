# -*- coding: utf-8 -*-
from rest_framework import serializers

from piglets.models import Piglets
from locations.models import Location


class PigletsSerializer(serializers.ModelSerializer):
    metatour_repr = serializers.ReadOnlyField()

    class Meta:
        model = Piglets
        fields = '__all__'


class PigletsSimpleSerializer(serializers.ModelSerializer):
    metatour_repr = serializers.ReadOnlyField()

    class Meta:
        model = Piglets
        fields = ['id', 'quantity', 'gilts_quantity', 'metatour_repr']


class MergeFromListRecordSerializer(serializers.Serializer):
    piglets_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    gilts_contains = serializers.BooleanField(default=False)
    changed = serializers.BooleanField(default=False)


class MergeFromListSerializer(serializers.Serializer):
    records = MergeFromListRecordSerializer(many=True)


class MovePigletsSerializer(serializers.Serializer):
    to_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    new_amount = serializers.IntegerField(required=False)
    gilts_contains = serializers.BooleanField(default=False)
    merge = serializers.BooleanField(default=False)