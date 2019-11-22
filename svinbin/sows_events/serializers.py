# -*- coding: utf-8 -*-
from rest_framework import serializers, status

from sows.models import Sow
from sows_events.models import Semination, Ultrasound, CullingSow, SowFarrow, AbortionSow
# from piglets_events.models import NewBornPigletsGroupRecount, NewBornPigletsMerger
from tours.models import Tour

from sows.serializers import SowSerializer

from core.utils import CustomValidation


class SeminationSerializer(serializers.ModelSerializer):
    sow = serializers.StringRelatedField()
    tour = serializers.StringRelatedField()

    class Meta:
        model = Semination
        fields = "__all__"


class SimpleSeminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semination
        fields = ['date', 'semination_employee', 'boar']


class CreateSeminationSerializer(serializers.ModelSerializer):
    week = serializers.IntegerField()

    class Meta:
        model = Semination
        fields = ['week', 'semination_employee', 'boar']


class UltrasoundSerializer(serializers.ModelSerializer):
    sow = SowSerializer()
    tour = serializers.StringRelatedField()

    class Meta:
        model = Ultrasound
        fields = "__all__"


class SimpleUltrasoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ultrasound
        fields = ['date', 'result', 'u_type']


class CreateUltrasoundSerializer(serializers.Serializer):
    result = serializers.BooleanField()
    days = serializers.IntegerField()


class CullingSowSerializer(serializers.ModelSerializer):
    sow = serializers.StringRelatedField()
    tour = serializers.StringRelatedField()

    class Meta:
        model = CullingSow
        fields = "__all__"


class CreateCullingSowSerializer(serializers.ModelSerializer):
    farm_id = serializers.IntegerField()

    class Meta:
        model = CullingSow
        fields = ('farm_id', 'culling_type',)


class CreateCullingSowPkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CullingSow
        fields = ('culling_type', 'reason')        
 

class CreateSowFarrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SowFarrow
        fields = ['alive_quantity', 'dead_quantity', 'mummy_quantity']


class SowFarrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SowFarrow
        fields = '__all__'


class SimpleSowFarrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SowFarrow
        fields = ['date', 'alive_quantity', 'dead_quantity', 'mummy_quantity']


class AbortionSowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbortionSow
        fields = '__all__'
