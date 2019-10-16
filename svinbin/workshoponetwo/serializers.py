# -*- coding: utf-8 -*-
from rest_framework import serializers, status

from core.utils import CustomValidation
from sows.models import Sow


class FarmIdSerializer(serializers.Serializer):
    farm_id = serializers.IntegerField()


class CreateFarmIdSerializer(serializers.Serializer):
    farm_id = serializers.IntegerField()

    def validate_farm_id(self, value):
    	if Sow.objects.filter(farm_id=value).first():
    		raise CustomValidation('Not unique farm_id', 
                'farm_id', status_code=status.HTTP_400_BAD_REQUEST)
    	return value


class MassSowCreateSerializer(serializers.Serializer):
	# sows = serializers.IntegerField(many=True)
	week = serializers.IntegerField()