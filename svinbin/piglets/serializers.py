# -*- coding: utf-8 -*-
from rest_framework import serializers

from piglets.models import Piglets
from locations.models import Location


class PigletsSerializer(serializers.ModelSerializer):
    metatour_repr = serializers.ReadOnlyField()

    class Meta:
        model = Piglets
        fields = '__all__'


class MergeFromListRecordSerializer(serializers.Serializer):
    piglets_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    gilts_contains = serializers.BooleanField()
    changed = serializers.BooleanField()


class MergeFromListSerializer(serializers.Serializer):
    is_gilts_part = serializers.BooleanField(default=False)
    records = MergeFromListRecordSerializer(many=True)


class MovePigletsSerializer(serializers.Serializer):
    to_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    new_amount = serializers.IntegerField(required=False)
    merge = serializers.BooleanField(default=False)