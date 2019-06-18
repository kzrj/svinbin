# -*- coding: utf-8 -*-
from rest_framework import serializers

from pigs.models import Sow
from events.models import Semination, Ultrasound, CullingSow, NewBornPigletsGroupRecount, NewBornPigletsMerger

from pigs.serializers import SowSerializer


class SeminationSerializer(serializers.ModelSerializer):
    sow = serializers.StringRelatedField()
    tour = serializers.StringRelatedField()

    class Meta:
        model = Semination
        fields = "__all__"


class CreateSeminationSerializer(serializers.Serializer):
    week = serializers.IntegerField()
    farm_id = serializers.IntegerField()


class UltrasoundSerializer(serializers.ModelSerializer):
    sow = SowSerializer()
    tour = serializers.StringRelatedField()

    class Meta:
        model = Ultrasound
        fields = "__all__"


class CreateUltrasoundSerializer(CreateSeminationSerializer):
    result = serializers.BooleanField()


class CullingSowSerializer(serializers.ModelSerializer):
    sow = SowSerializer()
    tour = serializers.StringRelatedField()

    class Meta:
        model = CullingSow
        fields = "__all__"


class CreateCullingSowSerializer(serializers.ModelSerializer):
    farm_id = serializers.IntegerField()

    class Meta:
        model = CullingSow
        fields = ('farm_id', 'culling_type')


class NewBornPigletsGroupRecountSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewBornPigletsGroupRecount
        fields = "__all__"


class NewBornPigletsGroupMerger(serializers.ModelSerializer):
    class Meta:
        model = NewBornPigletsMerger
        fields = "__all__"    