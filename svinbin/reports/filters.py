# -*- coding: utf-8 -*-
from django_filters import rest_framework as filters

from reports.models import ReportDate


class ReportDateFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = ReportDate
        fields = '__all__'
