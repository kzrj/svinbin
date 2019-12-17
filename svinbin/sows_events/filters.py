# -*- coding: utf-8 -*-
from django_filters import rest_framework as filters

from sows_events.models import SowFarrow


class SowFarrowFilter(filters.FilterSet):
    class Meta:
        model = SowFarrow
        fields = '__all__'
