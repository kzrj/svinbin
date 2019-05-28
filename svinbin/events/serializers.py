# -*- coding: utf-8 -*-
from rest_framework import serializers

from pigs.models import Sow


class SeminationSerializer(serializers.ModelSerializer):
    week = serializers.IntegerField()

    class Meta:
        model = Sow
        fields = ('farm_id', 'week')