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


class SowSimpleV2Serializer(serializers.ModelSerializer):
    status = serializers.StringRelatedField()
    tour = serializers.StringRelatedField()
    location = serializers.ReadOnlyField(source='get_location')

    class Meta:
        model = Sow
        fields = ['status', 'tour', 'farm_id', 'id', 'location']


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
    breed = serializers.StringRelatedField()
    
    class Meta:
        model = Boar
        fields = ['id', 'farm_id', 'birth_id', 'location', 'breed']


class BoarCreateSerializer(serializers.Serializer):
    farm_id = serializers.CharField()
    birth_id = serializers.CharField()
    breed = serializers.PrimaryKeyRelatedField(queryset=BoarBreed.objects.all())


class BoarBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoarBreed
        fields = ['id', 'title']


class LocationPkField(serializers.RelatedField):
    def to_representation(self, value):
        if value == 0:
            return None
        return Location.objects.get(pk=value).get_full_loc


class SowOperationSerializer(serializers.Serializer):
    op_date = serializers.DateTimeField()
    op_week = serializers.IntegerField()
    op_initiator = serializers.CharField()
    op_label = serializers.CharField()
    op_from_location = LocationPkField(read_only=True)
    op_to_location = LocationPkField(read_only=True)
    op_uzi_result = serializers.BooleanField()


class SowWithOpsSerializer(SowSerializer):
    last_operations = SowOperationSerializer(many=True)
