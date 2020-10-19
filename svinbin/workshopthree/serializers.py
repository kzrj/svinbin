# -*- coding: utf-8 -*-
from rest_framework import serializers, status
from core.utils import CustomValidation

from tours.models import Tour
from locations.models import Location
from sows_events.models import MarkAsGilt


class MarkSowAsNurseSerializer(serializers.Serializer):
    piglets_tour = serializers.PrimaryKeyRelatedField(queryset=Tour.objects.all(), required=False)


class MoveSowAndPigletsSerializer(serializers.Serializer):
    from_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    to_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())

    def validate(self, data):
        if not data['from_location'].get_sow:
            raise serializers.ValidationError(f"В клетке {data['from_location'].get_full_loc} нет \
             свиноматки")

        if not data['from_location'].get_piglets:
            raise serializers.ValidationError(f"В клетке {data['from_location'].get_full_loc} нет поросят")

        if not data['to_location'].is_empty:
            raise CustomValidation(f"Клетка {data['to_location'].get_full_loc} не пустая. Есть свиноматка или поросята", 
                'to_location', status_code=status.HTTP_400_BAD_REQUEST)

        return data


class MarkAsGiltCreateSerializer(serializers.Serializer):
    birth_id = serializers.CharField()
    date = serializers.DateField(format="%Y-%m-%d", required=False, default=None)


class MarkAsGiltSerializer(serializers.ModelSerializer):
    birth_id = serializers.ReadOnlyField(source='gilt.birth_id')
    week = serializers.ReadOnlyField(source='tour.week_number')
    sow_farm_id = serializers.ReadOnlyField(source='sow.farm_id')

    class Meta:
        model = MarkAsGilt
        fields = ['date', 'sow_farm_id', 'week', 'birth_id']