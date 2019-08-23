# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.contrib.auth.models import User
from django_filters import rest_framework as filters

from sows.models import Sow


class SowFilter(filters.FilterSet):
    by_workshop_number = filters.NumberFilter(field_name='location',
     method='filter_by_workshop_number')

    farm_id_starts = filters.NumberFilter(field_name='farm_id', lookup_expr='startswith')
    farm_id_contains = filters.NumberFilter(field_name='farm_id', lookup_expr='contains')
    farm_id_isnull = filters.BooleanFilter(field_name='farm_id', lookup_expr='isnull')
    status_title = filters.CharFilter(field_name='status__title', lookup_expr='exact')
    not_in_tour = filters.BooleanFilter(field_name='tour', lookup_expr='isnull')
    status_title_not = filters.CharFilter(field_name='status__title', 
        method='filter_status_title_not')

    def filter_by_workshop_number(self, queryset, name, value):
        return queryset.filter(location__workshop__number=value)

    def filter_status_title_not(self, queryset, name, value):
        return queryset.filter(~Q(status__title=value))

    class Meta:
        model = Sow
        fields = '__all__'
