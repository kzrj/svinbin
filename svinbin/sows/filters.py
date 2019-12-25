# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q, Prefetch, F
from django.contrib.auth.models import User
from django_filters import rest_framework as filters

from sows.models import Sow, SowStatus
from sows_events.models import Semination


class SowStatusChoiceNotInFilter(filters.ModelMultipleChoiceFilter):
    def filter(self, qs, value):
        if value:
            qs = qs.filter(~Q(status__in=value))
        return qs

class SowsToSeminateFilter(filters.ModelMultipleChoiceFilter):
    def filter(self, qs, value):
        if value:
            qs = qs.filter(~Q(status__title__in=
                ["Осеменена 1", "Осеменена 2", "Супорос 28", "Супорос 35"]))
        return qs


class SowFilter(filters.FilterSet):
    by_workshop_number = filters.NumberFilter(field_name='location',
        method='filter_by_workshop_number')

    by_section = filters.NumberFilter(field_name='location',
        method='filter_by_section')

    by_section_in_cell = filters.NumberFilter(field_name='location',
        method='filter_by_section_in_cell')

    farm_id_starts = filters.NumberFilter(field_name='farm_id', lookup_expr='startswith')
    farm_id_contains = filters.NumberFilter(field_name='farm_id', lookup_expr='contains')
    farm_id_isnull = filters.BooleanFilter(field_name='farm_id', lookup_expr='isnull')
    status_title = filters.CharFilter(field_name='status__title', lookup_expr='exact')
    status_title_in = filters.ModelMultipleChoiceFilter(
        field_name='status__title',
        to_field_name='title',
        queryset=SowStatus.objects.all(),
    )
    status_title_not_in = SowStatusChoiceNotInFilter(
        field_name='status__title',
        to_field_name='title',
        queryset=SowStatus.objects.all())

    to_seminate = filters.BooleanFilter(
        field_name='status__title',
        method='filter_to_seminate')

    not_in_tour = filters.BooleanFilter(field_name='tour', lookup_expr='isnull')

    all_in_workshop_number = filters.NumberFilter(field_name='location',
        method='filter_all_in_workshop_number')

    # created_at_gt = filters.Da

    def filter_by_section(self, queryset, name, value):
        return queryset.filter(location__section__pk=value)

    def filter_by_section_in_cell(self, queryset, name, value):
        return queryset.filter(location__sowAndPigletsCell__isnull=False,
         	location__sowAndPigletsCell__section__pk=value)

    def filter_by_workshop_number(self, queryset, name, value):
        return queryset.filter(location__workshop__number=value)

    def filter_to_seminate(self, queryset, name, value):
        if value:
            queryset = queryset.filter(~Q(status__title__in=
                ["Осеменена 1", "Осеменена 2", "Супорос 28", "Супорос 35"]))
        return queryset

    def filter_all_in_workshop_number(self, queryset, name, value):
        return queryset.get_all_sows_in_workshop(value)

    class Meta:
        model = Sow
        fields = '__all__'
