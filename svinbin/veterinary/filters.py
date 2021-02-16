# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_filters import rest_framework as filters

from veterinary.models import Recipe, PigletsVetEvent


class RecipeFilter(filters.FilterSet):
    class Meta:
        model = Recipe
        fields = '__all__'


class PigletsVetEventFilter(filters.FilterSet):
	# re_type = filters.CharFilter()

    class Meta:
        model = PigletsVetEvent
        fields = '__all__'