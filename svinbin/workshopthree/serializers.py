# -*- coding: utf-8 -*-
from rest_framework import serializers

import transactions.serializers as transactions_serializers
import sows.serializers as sows_serializers
from sows.models import Sow
from tours.models import Tour


class SowsIdsSerializer(serializers.Serializer):
    sows = serializers.PrimaryKeyRelatedField(queryset=Sow.objects.all(), many=True)


class NewGiltBirthIdSerializer(serializers.Serializer):
    birth_id = serializers.CharField()


class CreateRecountSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()


class MarkSowAsNurseSerializer(serializers.Serializer):
    piglets_tour = serializers.PrimaryKeyRelatedField(queryset=Tour.objects.all(), required=False)
