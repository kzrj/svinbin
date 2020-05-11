# -*- coding: utf-8 -*-
from rest_framework import serializers

from tours.models import Tour


class MarkSowAsNurseSerializer(serializers.Serializer):
    piglets_tour = serializers.PrimaryKeyRelatedField(queryset=Tour.objects.all(), required=False)