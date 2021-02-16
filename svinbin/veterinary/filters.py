# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_filters import rest_framework as filters

from veterinary.models import Recipe, PigletsVetEvent
from tours.filters import NumberInFilter


class RecipeFilter(filters.FilterSet):
    class Meta:
        model = Recipe
        fields = '__all__'


class PigletsVetEventFilter(filters.FilterSet):
	ru_type = filters.CharFilter(method='filter_ru_type')
	sections = NumberInFilter(field_name='location__id', lookup_expr='in')
	tours = NumberInFilter(field_name='week_tour__id', lookup_expr='in')

	def filter_ru_type(self, queryset, name, value):
        return queryset.filter(recipe__med_type=value)

    class Meta:
        model = PigletsVetEvent
        fields = '__all__'