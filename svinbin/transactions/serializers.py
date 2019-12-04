# -*- coding: utf-8 -*-
from rest_framework import serializers

from transactions.models import SowTransaction, PigletsTransaction


class SowTransactionSerializer(serializers.ModelSerializer):
    from_location = serializers.StringRelatedField()
    to_location = serializers.StringRelatedField()
    sow = serializers.StringRelatedField()

    class Meta:
        model = SowTransaction  
        fields = '__all__'


class PigletsTransactionSerializer(serializers.ModelSerializer):
    from_location = serializers.StringRelatedField()
    to_location = serializers.StringRelatedField()
    
    class Meta:
        model = PigletsTransaction
        fields = '__all__'