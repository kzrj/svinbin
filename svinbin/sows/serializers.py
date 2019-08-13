# -*- coding: utf-8 -*-
from rest_framework import serializers, status

from sows.models import Sow
from locations.models import Location


class SowSerializer(serializers.ModelSerializer):
    location = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    tour = serializers.StringRelatedField()
    status = serializers.StringRelatedField()

    # seminations in current tour
    # ultrasounds in current tour

    class Meta:
        model = Sow
        fields = '__all__'


class SowSimpleSerializer(serializers.ModelSerializer):
    status = serializers.StringRelatedField()
    tour = serializers.StringRelatedField()

    class Meta:
        model = Sow
        fields = ['status', 'tour', 'farm_id', 'birth_id', 'id']


class SowsToMoveSerializer(serializers.Serializer):
    # mb alive
    sows = serializers.PrimaryKeyRelatedField(queryset=Sow.objects.all(), many=True)
    to_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
