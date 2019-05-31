# -*- coding: utf-8 -*-
from rest_framework import serializers

from pigs.models import Sow


class SeminationSerializer(serializers.Serializer):
    week = serializers.IntegerField()
    farm_id = serializers.IntegerField()


class UltrasoundSerializer(SeminationSerializer)
    result = serializers.BooleanField()