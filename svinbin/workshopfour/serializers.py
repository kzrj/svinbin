# -*- coding: utf-8 -*-
from rest_framework import serializers

from workshops.models import PigletsGroupCell


class MoveFromCellToCellSerializer(serializers.Serializer):
	from_cell = serializers.PrimaryKeyRelatedField(queryset=PigletsGroupCell.objects.all())
	to_cell = serializers.PrimaryKeyRelatedField(queryset=PigletsGroupCell.objects.all())
	quantity = serializers.IntegerField()