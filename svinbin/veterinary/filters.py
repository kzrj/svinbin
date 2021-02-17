# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q

from django_filters import rest_framework as filters

from veterinary.models import Recipe, PigletsVetEvent
from tours.filters import NumberInFilter


class RecipeFilter(filters.FilterSet):
    class Meta:
        model = Recipe
        fields = '__all__'


class PigletsVetEventFilter(filters.FilterSet):
    sections = NumberInFilter(method='filter_sections')
    med_type = filters.CharFilter(field_name='recipe__med_type', lookup_expr='exact')
    date = filters.DateFromToRangeFilter()

    def filter_sections(self, queryset, name, value):
        return queryset.filter(Q(
            Q(location__pigletsGroupCell__section__pk__in=value) |
            Q(location__sowAndPigletsCell__section__pk__in=value)
            ))

    class Meta:
        model = PigletsVetEvent
        fields = '__all__'