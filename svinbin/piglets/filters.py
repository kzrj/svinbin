# # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django_filters import rest_framework as filters

from piglets.models import Piglets


class PigletsFilter(filters.FilterSet):
    status_title = filters.CharFilter(field_name='status__title', lookup_expr='exact')
    not_status_title = filters.CharFilter(field_name='status__title', method='filter_not_status_title')

    by_workshop_number = filters.NumberFilter(field_name='location',
     method='filter_by_workshop_number')

    piglets_with_weighing_record = filters.CharFilter(field_name='with_weighing_records',
        method='filter_piglets_with_weighing_record')

    piglets_without_weighing_record = filters.CharFilter(field_name='without_weighing_records',
        method='filter_piglets_without_weighing_record')

    def filter_not_status_title(self, queryset, name, value):
        return queryset.filter(~Q(status__title=value))

    def filter_by_workshop_number(self, queryset, name, value):
        return queryset.filter(location__workshop__number=value)

    def filter_piglets_with_weighing_record(self, queryset, name, value):
        return queryset.piglets_with_weighing_record(value)

    def filter_piglets_without_weighing_record(self, queryset, name, value):
        return queryset.piglets_without_weighing_record(value)

    class Meta:
        model = Piglets
        fields = '__all__'
