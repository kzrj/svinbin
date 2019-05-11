# -*- coding: utf-8 -*-
from rest_framework import serializers, status

from transactions.models import SowTransaction


class MoveToWorshopOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = SowTransaction
        fields = ('sow',)


class PutSowInCellSerializer(serializers.ModelSerializer):
    cell_number = serializers.CharField()
    # need validation

    class Meta:
        model = SowTransaction
        fields = ('sow', 'cell_number')