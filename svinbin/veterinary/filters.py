# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_filters import rest_framework as filters

from veterinary.models import Recipe


class RecipeFilter(filters.FilterSet):
    class Meta:
        model = Recipe
        fields = '__all__'