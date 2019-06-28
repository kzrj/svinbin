# -*- coding: utf-8 -*-
from rest_framework import serializers

from locations.models import PigletsGroupCell


class MoveFromCellToCellSerializer(serializers.Serializer):
	from_cell = serializers.PrimaryKeyRelatedField(queryset=PigletsGroupCell.objects.all())
	to_cell = serializers.PrimaryKeyRelatedField(queryset=PigletsGroupCell.objects.all())
	quantity = serializers.IntegerField()