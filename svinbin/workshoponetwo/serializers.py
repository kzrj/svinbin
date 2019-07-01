# -*- coding: utf-8 -*-
from rest_framework import serializers


class FarmIdSerializer(serializers.Serializer):
    farm_id = serializers.IntegerField()