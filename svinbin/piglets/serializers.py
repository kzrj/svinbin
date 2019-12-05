# -*- coding: utf-8 -*-
from rest_framework import serializers

from piglets.models import Piglets
# from locations.models import Location


class PigletsSerializer(serializers.ModelSerializer):
    metatour_repr = serializers.ReadOnlyField()

    class Meta:
        model = Piglets
        fields = '__all__'


class MergeFromListRecordSerializer(serializers.Serializer):
    piglets_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    changed = serializers.BooleanField()


# class MoveFromCellToCellSerializer(serializers.Serializer):
#     from_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
#     to_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
#     quantity = serializers.IntegerField()
#     gilts_quantity = serializers.IntegerField(default=0)


# class MoveToSerializer(serializers.Serializer):
#     to_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
#     quantity = serializers.IntegerField()
#     gilts_quantity = serializers.IntegerField(default=0)
