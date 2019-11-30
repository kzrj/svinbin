# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.contrib.auth.models import User
from django_filters import rest_framework as filters

from locations.models import Location, Section


class LocationFilter(filters.FilterSet):
    sowAndPigletsCell = filters.BooleanFilter(field_name='sowAndPigletsCell',
     lookup_expr='isnull', exclude=True)
    pigletsGroupCell = filters.BooleanFilter(field_name='pigletsGroupCell',
     lookup_expr='isnull', exclude=True)

    by_workshop = filters.NumberFilter(field_name='workshop', method='filter_by_workshop')

    by_section = filters.NumberFilter(field_name='section', method='filter_by_section')

    sections_by_workshop_number = filters.NumberFilter(field_name='section',
         method='filter_by_sections_by_workshop_number')

    def filter_by_workshop(self, queryset, name, value):
        return queryset.filter(Q(
            Q(workshop__pk=value) |
            Q(section__workshop__pk=value) |
            Q(sowAndPigletsCell__workshop__pk=value) |
            Q(pigletsGroupCell__workshop__pk=value)
            ))

    def filter_by_section(self, queryset, name, value):
        return queryset.filter(Q(
            Q(section__pk=value) |
            Q(sowAndPigletsCell__section__pk=value) |
            Q(pigletsGroupCell__section__pk=value)
            ))

    def filter_by_sections_by_workshop_number(self, queryset, name, value):
        return queryset.filter(section__workshop__number=value)

    class Meta:
        model = Location
        fields = '__all__'


class SectionFilter(filters.FilterSet):
    class Meta:
        model = Section
        fields = '__all__'
