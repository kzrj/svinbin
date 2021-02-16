# -*- coding: utf-8 -*-
from rest_framework import serializers

import sows.serializers as sows_serializers
import piglets.serializers as piglets_serializers
import veterinary.serializers as veterinary_serializers

from locations.models import Location, Section


class SectionSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Section
        exclude = ['created_at', 'modified_at' ]


class SectionFilterSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(read_only=True)
    workshop = serializers.StringRelatedKey(read_only=True)
    
    class Meta:
        model = Section
        exclude = ['created_at', 'modified_at' ]  


class LocationPKSerializer(serializers.Serializer):
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())


class LocationCellSerializer(serializers.ModelSerializer):
    cell = serializers.ReadOnlyField(source='get_cell_number')

    sow_set = sows_serializers.SowSimpleSerializer(many=True, read_only=True)
    piglets = piglets_serializers.PigletsSimpleSerializer(many=True, read_only=True)

    is_empty = serializers.ReadOnlyField()
    is_sow_empty = serializers.ReadOnlyField()
    is_piglets_empty = serializers.ReadOnlyField()

    class Meta:
        model = Location
        fields = [
            'id',
            'cell',
            'sow_set',
            'piglets',
            'is_empty',
            'is_sow_empty',
            'is_piglets_empty']


class LocationPigletsCellSerializer(serializers.ModelSerializer):
    cell = serializers.ReadOnlyField(source='get_cell_number')
    piglets = piglets_serializers.PigletsSimpleSerializer(many=True, read_only=True)
    is_piglets_empty = serializers.ReadOnlyField()

    class Meta:
        model = Location
        fields = [
            'id',
            'cell',
            'piglets',
            'is_piglets_empty']


class LocationPigletsVetCellSerializer(serializers.ModelSerializer):
    cell = serializers.ReadOnlyField(source='get_cell_number')
    piglets = veterinary_serializers.PigletsVetEventsSerializer(many=True, read_only=True)
    is_piglets_empty = serializers.ReadOnlyField()

    class Meta:
        model = Location
        fields = [
            'id',
            'cell',
            'piglets',
            'is_piglets_empty']


class LocationSowCellSerializer(serializers.ModelSerializer):
    cell = serializers.ReadOnlyField(source='get_cell_number')
    sow_set = sows_serializers.SowSimpleSerializer(many=True, read_only=True)
    is_sow_empty = serializers.ReadOnlyField()

    class Meta:
        model = Location
        fields = [
            'id',
            'cell',
            'sow_set',
            'is_sow_empty',
            ]


class LocationSectionSerializer(serializers.ModelSerializer):
    section_number = serializers.ReadOnlyField(source='section.number')
    section_id = serializers.ReadOnlyField(source='section.id')
    section_name = serializers.ReadOnlyField(source='section.name')

    # created via aggregation in queryset method 
    pigs_count = serializers.ReadOnlyField() 

    class Meta:
        model = Location
        fields = ['id', 'section_number', 'section_id', 'pigs_count', 'section_name']
