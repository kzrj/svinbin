# -*- coding: utf-8 -*-
from rest_framework import serializers, status

from piglets.models import NomadPigletsGroup, NewBornPigletsGroup


class NomadPigletsGroupPkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NomadPigletsGroup
        fields = ('pk',)


class NomadPigletsGroupSerializer(serializers.ModelSerializer):
    creating_new_born_merger = serializers.StringRelatedField()
    status = serializers.StringRelatedField()

    class Meta:
        model = NomadPigletsGroup
        
        fields = ['id', 'start_quantity', 'quantity', 'active', 'location',
         'split_record', 'groups_merger', 'creating_new_born_merger', 'status' ,'creating_nomad_merger',
         'gilt_quantity']


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