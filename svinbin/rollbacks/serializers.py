# -*- coding: utf-8 -*-
from rest_framework import serializers

from rollbacks.models import Rollback


class RollbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rollback
        fields = '__all__'

