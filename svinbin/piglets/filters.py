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

    piglets_with_weighing_record = filters.CharFilter(field_name='weighing_records',
        method='piglets_with_weighing_record')

    piglets_without_weighing_record = filters.CharFilter(field_name='weighing_records',
        method='piglets_without_weighing_record')

    def filter_by_workshop_number(self, queryset, name, value):
        return queryset.filter(location__workshop__number=value)

    def piglets_with_weighing_record(self, queryset, name, value):
        return queryset.piglets_with_weighing_record(value)

    def piglets_without_weighing_record(self, queryset, name, value):
        return queryset.piglets_without_weighing_record(value)

    class Meta:
        model = NomadPigletsGroup
        fields = '__all__'
