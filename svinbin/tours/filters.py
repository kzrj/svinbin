# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.contrib.auth.models import User
from django_filters import rest_framework as filters

from tours.models import Tour


class TourFilter(filters.FilterSet):
    by_workshop_number = filters.NumberFilter(field_name='location',
     method='filter_by_workshop_number')

    active = filters.BooleanField(method='filter_active')

    # farm_id startswith
    # birth_id startswith

    def filter_by_workshop_number(self, queryset, name, value):
        return queryset.filter(location__workshop__number=value)

    def filter_active(self, queryset, value):
    	if value:
    		return queryset.filter()




    class Meta:
        model = Tour
        fields = '__all__'
