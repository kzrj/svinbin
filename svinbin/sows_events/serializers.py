# -*- coding: utf-8 -*-
from rest_framework import serializers

from sows_events.models import Semination, Ultrasound, CullingSow, SowFarrow, AbortionSow, CullingBoar, SemenBoar

from sows.serializers import SowSerializer, BoarSerializer


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
        fields = ('farm_id', 'culling_type', )


class CreateCullingSowPkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CullingSow
        fields = ('culling_type', 'reason' , 'weight')        
 

class CreateSowFarrowSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = SowFarrow
        fields = ['alive_quantity', 'dead_quantity', 'mummy_quantity', 'date']


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


class CullingBoarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CullingBoar
        fields = ('culling_type', 'reason', 'weight')


class SemenBoarCreateSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = SemenBoar
        fields = ('a', 'b', 'd', 'morphology_score', 'final_motility_score', 'date')


class SemenBoarSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%d")
    boar = BoarSerializer()

    class Meta:
        model = SemenBoar
        exclude = ('created_at', 'modified_at', 'id')
