# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q, Prefetch, F
from django.contrib.auth.models import User
from django_filters import rest_framework as filters

from sows.models import Sow
from sows_events.models import Semination


class SowFilter(filters.FilterSet):
    by_workshop_number = filters.NumberFilter(field_name='location',
     method='filter_by_workshop_number')

    farm_id_starts = filters.NumberFilter(field_name='farm_id', lookup_expr='startswith')
    farm_id_contains = filters.NumberFilter(field_name='farm_id', lookup_expr='contains')
    farm_id_isnull = filters.BooleanFilter(field_name='farm_id', lookup_expr='isnull')
    status_title = filters.CharFilter(field_name='status__title', lookup_expr='exact')
    status_title_in = filters.CharFilter(field_name='status__title', lookup_expr='in')

    not_in_tour = filters.BooleanFilter(field_name='tour', lookup_expr='isnull')
    status_title_not = filters.CharFilter(field_name='status__title', 
        method='filter_status_title_not')
    status_title_not_contains = filters.CharFilter(field_name='status__title', 
        method='filter_status_title_not_contains')
    suporos = filters.NumberFilter(field_name='suporos_30', 
        method='filter_suporos')

    seminated = filters.NumberFilter(field_name='seminated', 
        method='filter_seminated')

    def filter_by_workshop_number(self, queryset, name, value):
        return queryset.filter(location__workshop__number=value)

    def filter_status_title_not(self, queryset, name, value):
        return queryset.filter(~Q(status__title=value))

    def filter_status_title_not_contains(self, queryset, name, value):
        return queryset.filter(~Q(status__title__contains=value))

    def filter_suporos(self, queryset, name, value):
        if value == 30:
            # tested in sow model manager         
            return queryset.filter(
                ~Q(ultrasound__u_type__days=60),
                tour__isnull=False,
                ultrasound__u_type__days=30,
                # ultrasound__tour=F('tour'),
                # ultrasound__result=True,
            )
        if value == 60:
            # tested in sow model manager         
            return queryset.filter(
                sowfarrow__sow__farm_id__isnull=True,
                tour__isnull=False,
                ultrasound__u_type__days=60,
            )
        if not value:
            return queryset

    def filter_seminated(self, queryset, name, value):
        if value == 0:
            return queryset.filter(tour__isnull=True, farm_id__isnull=False)

        if value == 1:
            sows = list()       
            sows_init_qs = queryset.filter(
                ultrasound__sow__farm_id__isnull=True,
                sowfarrow__sow__farm_id__isnull=True,
                tour__isnull=False,
                ).prefetch_related(
                    Prefetch(
                         'semination_set',
                          queryset=Semination.objects.filter(tour=F('tour')),
                          to_attr="seminations_by_current_tour"
                        )
                )
            for sow in sows_init_qs:
                if len(sow.seminations_by_current_tour) == 1:
                    sows.append(sow.pk)
            return sows_init_qs.filter(pk__in=sows)
            
        if value == 2:
            sows = list()       
            sows_init_qs = queryset.filter(
                ultrasound__sow__farm_id__isnull=True,
                sowfarrow__sow__farm_id__isnull=True,
                tour__isnull=False,
                ).prefetch_related(
                    Prefetch(
                         'semination_set',
                          queryset=Semination.objects.filter(tour=F('tour')),
                          to_attr="seminations_by_current_tour"
                        )
                )
            for sow in sows_init_qs:
                if len(sow.seminations_by_current_tour) == 2:
                    sows.append(sow.pk)
            return sows_init_qs.filter(pk__in=sows)

        if not value:
            return queryset


    class Meta:
        model = Sow
        fields = '__all__'
