# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework import serializers, status


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
