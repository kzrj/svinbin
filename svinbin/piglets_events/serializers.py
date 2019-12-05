# # -*- coding: utf-8 -*-
from rest_framework import serializers

from piglets_events import models


class CullingPigletsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CullingPiglets
        fields = ['culling_type', 'reason']