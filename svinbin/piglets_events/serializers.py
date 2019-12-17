# # -*- coding: utf-8 -*-
from rest_framework import serializers

from piglets_events import models


class CullingPigletsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CullingPiglets
        fields = ['culling_type', 'reason']


class WeighingPigletsCreateSerializer(serializers.ModelSerializer):
	# quantity = serializers.InregerField(required=False)

    class Meta:
        model = models.WeighingPiglets
        fields = ['total_weight', 'place']


class WeighingPigletsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WeighingPiglets
        fields = '__all__'