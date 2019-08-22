# -*- coding: utf-8 -*-
from rest_framework import serializers, status

# from sows_events.serializers import SeminationSerializer
# import sows_events.serializers as sows_events_serializers
from sows.models import Sow, Boar
from sows_events.models import Semination
from locations.models import Location


class BoarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boar
        fields = '__all__'


class SowSerializer(serializers.ModelSerializer):
    location = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    tour = serializers.StringRelatedField()
    status = serializers.StringRelatedField()

    # seminations in current tour
    # ultrasounds in current tour

    # seminations = serializers.SerializerMethodField()

    class Meta:
        model = Sow
        fields = '__all__'

    # def get_seminations(self, obj):
    #     seminations_qs = obj.semination_set.all()
    #     return SowSeminationSerializer(seminations_qs, many=True).data


class SowSeminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semination
        # fields = '__all__'
        exclude = ['created_at', 'modified_at', 'sow', 'id']


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
