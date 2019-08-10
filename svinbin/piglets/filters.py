# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.contrib.auth.models import User
from django_filters import rest_framework as filters

from piglets.models import NomadPigletsGroup


class NomadPigletsGroupFilter(filters.FilterSet):
    status_title = filters.CharFilter(field_name='status__title', lookup_expr='exact')

    by_workshop_number = filters.NumberFilter(field_name='location',
     method='filter_by_workshop_number')

    by_weighing_place = filters.CharFilter(field_name='weighing_records',
        method='filter_by_weighing_place')

    def filter_by_workshop_number(self, queryset, name, value):
        return queryset.filter(location__workshop__number=value)

    def filter_by_weighing_place(self, queryset, name, value):
        return queryset.filter(weighing_records__place=value)

    class Meta:
        model = NomadPigletsGroup
        fields = '__all__'
