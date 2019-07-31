# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.contrib.auth.models import User
from django_filters import rest_framework as filters

from piglets.models import NomadPigletsGroup


class NomadPigletsGroupFilter(filters.FilterSet):
    class Meta:
        model = NomadPigletsGroup
        fields = '__all__'
