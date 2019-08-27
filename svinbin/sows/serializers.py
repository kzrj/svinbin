# -*- coding: utf-8 -*-
from rest_framework import serializers, status

# from sows_events.serializers import SeminationSerializer
# import sows_events.serializers as sows_events_serializers

from core.utils import CustomValidation
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


# Init only
class InitOnlyCreateSow(serializers.Serializer):
    farm_id = serializers.IntegerField()
    week = serializers.IntegerField()

    def validate_farm_id(self, value):
        if Sow.objects.filter(farm_id=value).first():
            raise CustomValidation('Not unique farm_id', 
                'farm_id', status_code=status.HTTP_400_BAD_REQUEST)
        return value


class InitOnlyCreateSeminatedSow(InitOnlyCreateSow):
    boar = serializers.IntegerField(required=False)


class InitOnlyCreateUltrasoundedSow(InitOnlyCreateSeminatedSow):    
    result = serializers.BooleanField()
    days = serializers.IntegerField()
    workshop_number = serializers.IntegerField()


class InitOnlyCreateSuporosWs3Sow(InitOnlyCreateSeminatedSow):
    section = serializers.IntegerField()
    cell = serializers.IntegerField()


class InitOnlyCreateFarrowSow(InitOnlyCreateSeminatedSow):    
    alive_quantity = serializers.IntegerField()
    dead_quantity = serializers.IntegerField()
    mummy_quantity = serializers.IntegerField()
    section = serializers.IntegerField()
    cell = serializers.IntegerField()