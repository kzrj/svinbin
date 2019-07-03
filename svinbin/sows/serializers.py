# -*- coding: utf-8 -*-
from rest_framework import serializers, status

from sows.models import Sow


class SowSerializer(serializers.ModelSerializer):
    location = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    tour = serializers.StringRelatedField()
    status = serializers.StringRelatedField()

    class Meta:
        model = Sow
        fields = '__all__'


class SowSimpleSerializer(serializers.ModelSerializer):
    status = serializers.StringRelatedField()
    tour = serializers.StringRelatedField()

    class Meta:
        model = Sow
        fields = ['status', 'tour', 'farm_id', 'birth_id', 'id']
