# -*- coding: utf-8 -*-
from rest_framework import serializers

from locations.models import Location


class MoveFromCellToCellSerializer(serializers.Serializer):
    from_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    to_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    quantity = serializers.IntegerField()
    gilts_quantity = serializers.IntegerField(default=0)


class MoveToSerializer(serializers.Serializer):
    to_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    quantity = serializers.IntegerField()
    gilts_quantity = serializers.IntegerField(default=0)