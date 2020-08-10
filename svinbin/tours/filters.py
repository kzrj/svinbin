# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.contrib.auth.models import User
from django_filters import rest_framework as filters

from tours.models import Tour
from sows.models import Sow


class TourFilter(filters.FilterSet):
    by_workshop_number = filters.NumberFilter(method='filter_by_workshop_number')

    def filter_by_workshop_number(self, queryset, name, value):
        pks = Sow.objects.all().get_tours_pks(workshop_number=value)
        return queryset.filter(pk__in=pks)

    class Meta:
        model = Tour
        fields = '__all__'
