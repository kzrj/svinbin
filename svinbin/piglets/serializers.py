# -*- coding: utf-8 -*-
import datetime

from rest_framework import serializers

from piglets.models import Piglets
from locations.models import Location


class PigletsSerializer(serializers.ModelSerializer):
    metatour_repr = serializers.ReadOnlyField()

    class Meta:
        model = Piglets
        fields = '__all__'


class PigletsSimpleSerializer(serializers.ModelSerializer):
    metatour_repr = serializers.ReadOnlyField()
    week_tour = serializers.StringRelatedField(source='metatour.week_tour')
    age = serializers.DurationField()

    class Meta:
        model = Piglets
        fields = ['id', 'quantity', 'gilts_quantity', 'metatour_repr', 'transfer_part_number', 
            'birthday', 'week_tour', 'age']


class MergeFromListRecordSerializer(serializers.Serializer):
    piglets_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    gilts_contains = serializers.BooleanField(default=False)
    gilt_quantity = serializers.IntegerField(required=False, default=0)
    changed = serializers.BooleanField(default=False)


class MergeFromListSerializer(serializers.Serializer):
    transfer_part_number = serializers.IntegerField(required=False, allow_null=True)
    records = MergeFromListRecordSerializer(many=True)


class MovePigletsSerializer(serializers.Serializer):
    to_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    new_amount = serializers.IntegerField(required=False)
    gilts_contains = serializers.BooleanField(default=False, required=False, allow_null=True)
    merge = serializers.BooleanField(default=False)


class MoveGiltsToWs12Serializer(serializers.Serializer):
    new_amount = serializers.IntegerField(allow_null=True, default=None)


class InitPigletsSerializer(serializers.Serializer):
    farrow_date = serializers.CharField()
    from_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(),
     required=False, allow_null=True)
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    quantity = serializers.IntegerField()
    gilts_quantity = serializers.IntegerField(required=False, allow_null=True)

    transaction_date = serializers.CharField(required=False, allow_null=True)

    def validate_transaction_date(self, value):
        if isinstance(value, str):
            return datetime.datetime.strptime(value, '%Y-%m-%d')
        return None