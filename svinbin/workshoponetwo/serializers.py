# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework import serializers, status

from core.utils import CustomValidation
from sows.models import Sow, Boar


class CreateFarmIdSerializer(serializers.Serializer):
    farm_id = serializers.IntegerField()

    def validate_farm_id(self, value):
        if Sow.objects.filter(farm_id=value).first():
            raise CustomValidation('Not unique farm_id', 
                'farm_id', status_code=status.HTTP_400_BAD_REQUEST)
        return value


class DoubleSeminationSerializer(serializers.Serializer):
    week = serializers.IntegerField()
    boar1 = serializers.PrimaryKeyRelatedField(queryset=Boar.objects.all())
    boar2 = serializers.PrimaryKeyRelatedField(queryset=Boar.objects.all())
    semination_employee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(employee__is_seminator=True))


class ImportSeminationsFile(serializers.Serializer):
    file = serializers.FileField(max_length=None, use_url=False)