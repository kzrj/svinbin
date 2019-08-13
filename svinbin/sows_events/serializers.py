# -*- coding: utf-8 -*-
from rest_framework import serializers, status

from sows.models import Sow
from sows_events.models import Semination, Ultrasound, CullingSow, SowFarrow
from piglets_events.models import NewBornPigletsGroupRecount, NewBornPigletsMerger
from tours.models import Tour

from sows.serializers import SowSerializer

from core.utils import CustomValidation


class SeminationSerializer(serializers.ModelSerializer):
    sow = serializers.StringRelatedField()
    tour = serializers.StringRelatedField()

    class Meta:
        model = Semination
        fields = "__all__"


# class CreateSeminationSerializer(serializers.Serializer):
#     week = serializers.IntegerField()
#     farm_id = serializers.IntegerField()


class CreateSeminationSerializer(serializers.ModelSerializer):
    week = serializers.IntegerField()

    class Meta:
        model = Semination
        fields = ['week', 'semination_employee']
    


class UltrasoundSerializer(serializers.ModelSerializer):
    sow = SowSerializer()
    tour = serializers.StringRelatedField()

    class Meta:
        model = Ultrasound
        fields = "__all__"


# class CreateUltrasoundSerializer(CreateSeminationSerializer):
#     result = serializers.BooleanField()


class CreateUltrasoundSerializer(serializers.Serializer):
    # week = serializers.IntegerField()
    result = serializers.BooleanField()


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
    # week = serializers.IntegerField()

    # def validate_week(self, value):
    #     # get tour with week in current year
    #     if Tour.objects.filter(week_number=value).first():
    #         return value
    #     else:
    #         raise CustomValidation('There is no tour with this week number.', 
    #             'week', status_code=status.HTTP_400_BAD_REQUEST)

    class Meta:
        model = SowFarrow
        fields = ['alive_quantity', 'dead_quantity', 'mummy_quantity', 'week']


class SowFarrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SowFarrow
        fields = '__all__'