# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.contrib.auth.models import User
from django_filters import rest_framework as filters

from tours.models import Tour
from sows.models import Sow
from piglets_events.models import WeighingPiglets


class TourFilter(filters.FilterSet):
    by_workshop_number = filters.NumberFilter(method='filter_by_workshop_number')
    has_weights = filters.BooleanFilter(method='filter_has_weights')
    has_weights_in_range = filters.DateFromToRangeFilter(method='filter_has_weights_in_range')
    has_weights_in_ws = filters.CharFilter(method='filter_has_weights_in_ws')
    year = filters.NumberFilter(field_name="year", lookup_expr='exact')

    def filter_by_workshop_number(self, queryset, name, value):
        pks = Sow.objects.all().get_tours_pks(workshop_number=value)
        return queryset.filter(pk__in=pks)

    def filter_has_weights(self, queryset, name, value):
        if value:
            return queryset.filter(Q(
                    Q(first_date_3_4__isnull=False) |
                    Q(first_date_4_8__isnull=False) |
                    Q(first_date_8_5__isnull=False) |
                    Q(first_date_8_6__isnull=False) |
                    Q(first_date_8_7__isnull=False) |
                    Q(first_date_spec__isnull=False)
                ))
        return queryset.none()

    def filter_has_weights_in_range(self, queryset, name, date_range):
        date_range = (date_range.start, date_range.stop)
        return queryset.filter(Q(
                    Q(first_date_3_4__range=date_range) |
                    Q(first_date_4_8__range=date_range) |
                    Q(first_date_8_5__range=date_range) |
                    Q(first_date_8_6__range=date_range) |
                    Q(first_date_8_7__range=date_range) |
                    Q(first_date_spec__range=date_range)
                ))

    def filter_has_weights_in_ws(self, queryset, name, value):
        return queryset.filter(piglets_weights__place=value)

    class Meta:
        model = Tour
        fields = '__all__'
