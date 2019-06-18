# -*- coding: utf-8 -*-
from rest_framework import serializers, status

# from events import serializers as events_serializers
from pigs.models import Sow, NomadPigletsGroup, NewBornPigletsGroup


class SowSerializer(serializers.ModelSerializer):
    location = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    tour = serializers.StringRelatedField()

    class Meta:
        model = Sow
        fields = '__all__'


class NomadPigletsGroupPkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NomadPigletsGroup
        fields = ('pk',)


class NomadPigletsGroupSerializer(serializers.ModelSerializer):
    creating_new_born_merger = serializers.StringRelatedField()
    # creating_new_born_merger = events_serializers.NewBornPigletsGroupMerger()

    class Meta:
        model = NomadPigletsGroup
        # fields = '__all__'
        fields = ['id', 'start_quantity', 'quantity', 'active', 'location',
         'split_record', 'groups_merger', 'creating_new_born_merger']


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