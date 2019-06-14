# -*- coding: utf-8 -*-
from rest_framework import serializers, status

from pigs.models import Sow, NomadPigletsGroup


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

    class Meta:
        model = NomadPigletsGroup
        # fields = '__all__'
        fields = ['id', 'start_quantity', 'quantity', 'active', 'location',
         'split_record', 'groups_merger', 'creating_new_born_merger']