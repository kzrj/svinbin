# -*- coding: utf-8 -*-
from rest_framework import serializers, status

from core.utils import CustomValidation

import transactions.serializers as transactions_serializers
import sows.serializers as sows_serializers
import piglets.serializers as piglets_serializers
import piglets_events.serializers as piglets_events_serializers

from locations.models import PigletsGroupCell, SowAndPigletsCell, Location, WorkShop, Section


class WokrshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkShop
        exclude = ['created_at', 'modified_at' ]


class SectionSerializer(serializers.ModelSerializer):
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
    workshop = serializers.StringRelatedField()
    section = serializers.StringRelatedField()

    class Meta:
        model = PigletsGroupCell
        exclude = ['created_at', 'modified_at' ]


class PigletsGroupCellPkSerializer(serializers.Serializer):
    cell = serializers.PrimaryKeyRelatedField(queryset=PigletsGroupCell.objects.all())


class LocationPKSerializer(serializers.Serializer):
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())


class LocationsFromToSerializer(serializers.Serializer):
    from_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    to_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())


class LocationPigletsGrouspCellSerializer(serializers.ModelSerializer):
    pigletsGroupCell = serializers.StringRelatedField()

    class Meta:
        model = Location
        fields = ['id', 'pigletsGroupCell']


class LocationSerializer(serializers.ModelSerializer):
    workshop = serializers.StringRelatedField()
    section = serializers.StringRelatedField()
    sowAndPigletsCell = SowAndPigletsCellSerializer(read_only=True)
    pigletsGroupCell = PigletsGroupCellSerializer(read_only=True)

    sow_set = sows_serializers.SowSimpleSerializer(many=True, read_only=True)
    newbornpigletsgroup_set = piglets_serializers.NewBornPigletsGroupSerializer(many=True,
        read_only=True)
    nomadpigletsgroup_set = piglets_serializers.NomadPigletsGroupSerializer(many=True,
        read_only=True)

    is_empty = serializers.ReadOnlyField()
    is_sow_empty = serializers.ReadOnlyField()
    is_piglets_empty = serializers.ReadOnlyField()

    class Meta:
        model = Location
        exclude = ['created_at', 'modified_at' ]