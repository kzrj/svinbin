# -*- coding: utf-8 -*-
from django_filters import rest_framework as filters

from sows_events.models import SemenBoar

class SemenBoarFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = SemenBoar
        fields = '__all__'
