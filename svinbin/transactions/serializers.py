# -*- coding: utf-8 -*-
from django.db.models import FieldDoesNotExist

from rest_framework import serializers, status

from transactions.models import SowTransaction, Location, PigletsTransaction
from pigs.models import Sow, NomadPigletsGroup

import pigs.serializers as pigs_serializers


class LocationSerializer(serializers.ModelSerializer):
    workshop = serializers.StringRelatedField()
    section = serializers.StringRelatedField()
    pigletsGroupCell = serializers.StringRelatedField()

    class Meta:
        model = Location  
        fields = '__all__'


class LocationPigletsSerializer(serializers.ModelSerializer):
    pigletsGroupCell = serializers.StringRelatedField()
    nomadpigletsgroup = pigs_serializers.NomadPigletsGroupSerializer()

    class Meta:
        model = Location  
        fields = ['id', 'pigletsGroupCell', 'nomadpigletsgroup']


class NomadGroupsListingFromLocationsField(serializers.RelatedField):
    def to_representation(self, value):
        nomad_group = NomadPigletsGroup.objects.filter(location=value).first()
        if nomad_group:
            return pigs_serializers.NomadPigletsGroupSerializer(nomad_group).data
        return 'No group'
            

class SowTransactionSerializer(serializers.ModelSerializer):
    from_location = serializers.StringRelatedField()
    to_location = serializers.StringRelatedField()
    sow = serializers.StringRelatedField()

    class Meta:
        model = SowTransaction  
        fields = '__all__'


class SowFarmIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sow
        fields = ('farm_id',)


class SowFarmIdAndCellSerializer(serializers.Serializer):
    cell_number = serializers.IntegerField()
    farm_id = serializers.IntegerField()
    
    # class Meta:
    #     model = Sow
    #     fields = ('farm_id', 'cell_number')

# class MoveToSeminationRowSerializer(serializers.Serializer):
#     sows_farm_ids = SowFarmIdSerializer(many=True)


class WeekNumberSerializer(serializers.Serializer):
    week_number = serializers.IntegerField()


class FarmIdSerializer(serializers.Serializer):
    farm_id = serializers.IntegerField()


class MoveToSeminationRowSerializer(serializers.Serializer):
    sow_farm_id = serializers.IntegerField()


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


class NomadPigletsTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PigletsTransaction
        fields = '__all__'