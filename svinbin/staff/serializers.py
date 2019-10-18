# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework import serializers, status

from .models import WorkShopEmployee


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class WorkshopEmployeeSerializer(serializers.ModelSerializer):
	user = serializers.StringRelatedField()
	workshop_number = serializers.IntegerField(source='workshop.number')

	class Meta:
		model = WorkShopEmployee
		fields = ['user', 'workshop_number', 'is_officer', 'is_seminator']