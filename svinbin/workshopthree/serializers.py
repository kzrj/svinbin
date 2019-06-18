# -*- coding: utf-8 -*-
from rest_framework import serializers

import transactions.serializers as transactions_serializers
from piglets.models import NewBornPigletsGroup
from piglets_events.models import NewBornPigletsMerger


class NewBornPigletsGroupSizeSerializer(serializers.ModelSerializer):
    new_amount = serializers.IntegerField(required=False)

    class Meta:
        model = NewBornPigletsGroup
        fields = ['size_label', 'new_amount']


class NewBornPigletsGroupPkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewBornPigletsGroup
        fields = ['pk']


# class NewBornGroupsToMerge(serializers.Serializer):
#   groups = NewBornPigletsGroupPkSerializer(many=True)


class NewBornGroupsToMerge(serializers.ModelSerializer):
    # piglets_groups = serializers.PrimaryKeyRelatedField(many=True, queryset=NewBornPigletsGroup.objects.all())

    class Meta:
        model = NewBornPigletsMerger
        fields = ['piglets_groups', ]