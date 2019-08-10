# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    is_seminator = filters.BooleanFilter(field_name='employee__is_seminator')

    class Meta:
        model = User
        fields = '__all__'
