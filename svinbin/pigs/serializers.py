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
    class Meta:
        model = NomadPigletsGroup
        fields = '__all__'