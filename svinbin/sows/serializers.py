# -*- coding: utf-8 -*-
from rest_framework import serializers

from sows.models import Sow, Boar, Gilt, BoarBreed
from sows_events.models import Semination
from locations.models import Location


class SowSerializer(serializers.ModelSerializer):
    location = serializers.ReadOnlyField(source='get_location')
    status = serializers.StringRelatedField()
    tour = serializers.StringRelatedField()

    class Meta:
        model = Sow
        fields = '__all__'


class SowManySerializer(serializers.ModelSerializer):
    location = serializers.ReadOnlyField(source='get_location')
    status = serializers.StringRelatedField()
    tour = serializers.StringRelatedField()

    seminations_current_tour = serializers.ReadOnlyField(
        source='get_seminations_by_current_tour_values_list')

    ultrasound_30_current_tour = serializers.ReadOnlyField(
        source='get_ultrasound_30_by_current_tour_values_list')

    ultrasound_60_current_tour = serializers.ReadOnlyField(
        source='get_ultrasound_60_by_current_tour_values_list')

    class Meta:
        model = Sow
        fields = '__all__'


class SowSimpleSerializer(serializers.ModelSerializer):
    status = serializers.StringRelatedField()
    tour = serializers.StringRelatedField()

    class Meta:
        model = Sow
        fields = ['status', 'tour', 'farm_id', 'id']


class SowsToMoveSerializer(serializers.Serializer):
    # mb alive
    sows = serializers.PrimaryKeyRelatedField(queryset=Sow.objects.all(), many=True)
    to_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())


class SowsMassSeminationSerializer(serializers.ModelSerializer):
    sows = serializers.ListField(child=serializers.IntegerField())
    week = serializers.IntegerField()

    class Meta:
        model = Semination
        fields = ['sows', 'week', 'semination_employee', 'boar']


class SowsMassUltrasoundSerializer(serializers.Serializer):
    sows = serializers.ListField(child=serializers.IntegerField())
    days = serializers.IntegerField()
    result =serializers.BooleanField()  


class GiltSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gilt
        fields = '__all__'


class GiltCreateSerializer(serializers.Serializer):
    birth_id = serializers.CharField()
    mother_sow_farm_id = serializers.IntegerField()


class BoarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boar
        fields = ['id', 'birth_id', 'location', 'breed']


class BoarCreateSerializer(serializers.Serializer):
    birth_id = serializers.CharField()
    breed = serializers.PrimaryKeyRelatedField(queryset=BoarBreed.objects.all())


class BoarBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoarBreed
        fields = ['id', 'title']