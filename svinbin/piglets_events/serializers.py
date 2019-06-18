# -*- coding: utf-8 -*-
from rest_framework import serializers

from piglets_events import models


class NewBornPigletsGroupRecountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NewBornPigletsGroupRecount
        fields = "__all__"


class NewBornPigletsGroupMergerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NewBornPigletsMerger
        fields = "__all__"    


class CullingPigletsTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CullingNewBornPiglets
        fields = ['culling_type', 'reason']


class CullingNewBornPigletsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CullingNewBornPiglets
        fields = '__all__'