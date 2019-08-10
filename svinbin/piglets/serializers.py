# -*- coding: utf-8 -*-
from rest_framework import serializers, status

from piglets.models import NomadPigletsGroup, NewBornPigletsGroup
from piglets_events.serializers import WeighingPigletsSerializer


class NomadPigletsGroupPkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NomadPigletsGroup
        fields = ('pk',)


class NomadPigletsGroupSerializer(serializers.ModelSerializer):
    creating_new_born_merger = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    weighing_records = WeighingPigletsSerializer(many=True)

    class Meta:
        model = NomadPigletsGroup        
        fields = '__all__'


class NewBornPigletsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewBornPigletsGroup
        fields = "__all__"


class NewBornPigletsGroupPkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewBornPigletsGroup
        fields = ('pk',)


class NewBornPigletsGetSerializer(serializers.Serializer):
    new_born_group = serializers.IntegerField()