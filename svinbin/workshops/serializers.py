# -*- coding: utf-8 -*-
from rest_framework import serializers

import transactions.serializers as transactions_serializers

from workshops.models import PigletsGroupCell


class PigletsGroupCellSerializer(serializers.ModelSerializer):
    section = serializers.StringRelatedField()
    # locations = serializers.StringRelatedField(many=True)
    locations = transactions_serializers.NomadGroupsListingFromLocationsField(many=True, read_only=True)
    

    class Meta:
        model = PigletsGroupCell
        fields = ['id', 'section', 'number', 'locations']