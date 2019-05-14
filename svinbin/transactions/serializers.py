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


class PutPigletsInCellSerializer(serializers.Serializer):
    piglets_transaction_id = serializers.IntegerField()
    to_cell_number = serializers.IntegerField()
    quantity = serializers.IntegerField()
    
    class Meta:
        fields = ('piglets_transaction_id', 'quantity', 'to_cell_number')
