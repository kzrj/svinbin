# -*- coding: utf-8 -*-
from rest_framework import serializers, status

from core.utils import CustomValidation

import transactions.serializers as transactions_serializers
import sows.serializers as sows_serializers
import piglets.serializers as piglets_serializers
# import piglets_events.serializers as piglets_events_serializers

from locations.models import PigletsGroupCell, SowAndPigletsCell, Location, WorkShop, Section


class WokrshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkShop
        exclude = ['created_at', 'modified_at' ]


class SectionSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(read_only=True)
    # sows_count_by_tour = serializers.ReadOnlyField()
    # count_piglets = serializers.ReadOnlyField()

    class Meta:
        model = Section
        exclude = ['created_at', 'modified_at' ]


class SowAndPigletsCellSerializer(serializers.ModelSerializer):
    workshop = serializers.StringRelatedField()
    section = serializers.StringRelatedField()

    class Meta:
        model = SowAndPigletsCell
        exclude = ['created_at', 'modified_at' ]


class PigletsGroupCellSerializer(serializers.ModelSerializer):
    class Meta:
        model = PigletsGroupCell
        fields = ['number', 'section' ]    


class LocationPKSerializer(serializers.Serializer):
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())


class LocationsFromToSerializer(serializers.Serializer):
    from_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    to_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class LocationCellSerializer(serializers.ModelSerializer):
    cell = serializers.ReadOnlyField(source='get_cell_number')

    sow_set = sows_serializers.SowSimpleSerializer(many=True, read_only=True)
    piglets = piglets_serializers.PigletsSimpleSerializer(many=True, read_only=True)

    is_empty = serializers.ReadOnlyField()
    is_sow_empty = serializers.ReadOnlyField()
    is_piglets_empty = serializers.ReadOnlyField()

    class Meta:
        model = Location
        fields = ['id', 'cell', 'sow_set', 'piglets', 'is_empty', 'is_sow_empty', 'is_piglets_empty']


class LocationSectionSerializer(serializers.ModelSerializer):
    section_number = serializers.ReadOnlyField(source='section.number')
    section_id = serializers.ReadOnlyField(source='section.id')
    # count_piglets = serializers.ReadOnlyField()

    class Meta:
        model = Location
        fields = ['id', 'section_number', 'section_id']
