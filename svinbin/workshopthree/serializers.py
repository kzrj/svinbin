# -*- coding: utf-8 -*-
from rest_framework import serializers

import transactions.serializers as transactions_serializers
import sows.serializers as sows_serializers
from piglets.models import NewBornPigletsGroup
from piglets_events.models import NewBornPigletsMerger
from sows.models import Sow


class NewBornPigletsGroupSizeSerializer(serializers.ModelSerializer):
    new_amount = serializers.IntegerField(required=False)

    class Meta:
        model = NewBornPigletsGroup
        fields = ['size_label', 'new_amount']


class NewBornPigletsGroupPkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewBornPigletsGroup
        fields = ['pk']


class NewBornGroupsToMerge(serializers.Serializer):
    groups = serializers.PrimaryKeyRelatedField(queryset=NewBornPigletsGroup.objects.all(), many=True)


class NewBornGroupsToMerge(serializers.ModelSerializer):
    class Meta:
        model = NewBornPigletsMerger
        fields = ['piglets_groups', ]


class SowsIdsSerializer(serializers.Serializer):
    sows = serializers.PrimaryKeyRelatedField(queryset=Sow.objects.all(), many=True)
