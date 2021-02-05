# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework import serializers, status

from .models import WorkShopEmployee


class UserSerializer(serializers.ModelSerializer):
    farm_name = serializers.ReadOnlyField(source='employee.farm_name')

    class Meta:
        model = User
        # fields = "__all__"
        fields = ['id', 'username', 'farm_name']


class WorkshopEmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    workshop_number = serializers.IntegerField(source='workshop.number', allow_null=True)

    class Meta:
        model = WorkShopEmployee
        fields = ['user', 'workshop_number', 'is_officer', 'is_seminator', 'is_veterinar',
         'is_admin', 'is_operator']