# -*- coding: utf-8 -*-
from rest_framework import serializers, status

from core.utils import CustomValidation
import transactions.serializers as transactions_serializers
from locations.models import PigletsGroupCell, SowAndPigletsCell


class PigletsGroupCellSerializer(serializers.ModelSerializer):
    section = serializers.StringRelatedField()
    locations = transactions_serializers.NomadGroupsListingFromLocationsField(many=True, read_only=True)
    
    class Meta:
        model = PigletsGroupCell
        fields = ['id', 'section', 'number', 'locations']


class PigletsGroupCellPkSerializer(serializers.Serializer):
    cell = serializers.PrimaryKeyRelatedField(queryset=PigletsGroupCell.objects.all())


class SowAndPigletsCellSerializer(serializers.ModelSerializer):
    class Meta:
        model = SowAndPigletsCell
        fields = '__all__'


class SowAndPigletsCellIdSerializer(serializers.Serializer):
    cell_number = serializers.IntegerField()

    def validate_cell_number(self, value):
        if not SowAndPigletsCell.objects.filter(pk=value).first():
            raise CustomValidation('There is no cell with this number.', 
                'cell_number', status_code=status.HTTP_400_BAD_REQUEST) 
        return value