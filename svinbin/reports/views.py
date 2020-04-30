# -*- coding: utf-8 -*-
from datetime import timedelta, date

from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework import status, viewsets, pagination
from rest_framework.response import Response
from rest_framework.decorators import action

from tours.filters import TourFilter

from tours.models import Tour
from piglets.models import Piglets
from sows_events.models	import SowFarrow
from reports.models import ReportDate

from reports.serializers import ReportTourSerializer, AnnotateFieldsModelSerializer, ReportDateSerializer
from reports.filters import ReportDateFilter


class TourReportViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all() \
                .order_by('-year','week_number', ) \
                .add_sow_data() \
                .add_farrow_data() \
                .add_count_tour_sow() \
                .add_weight_date() \
                .add_week_weight() \
                .add_week_weight_ws8_v2() \
                .add_culling_data_by_week_tour() \
                .add_piglets_count_by_ws_week_tour() \
                .add_gilts_count_by_ws_week_tour() \
                .add_count_transfer_to_7_5()

    serializer_class = ReportTourSerializer
    filter_class = TourFilter


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data,
            'total_info': 'asdasdHUi'
            # 'total_info': total_info
        })


class ReportDateViewSet(viewsets.ModelViewSet):
    queryset = ReportDate.objects.all() \
                .add_today_sows_qnty() \
                .add_sows_quantity_at_date_start() \
                .add_sow_padej_qnty() \
                .add_sow_vinuzhd_qnty() \
                .add_sows_quantity_at_date_end() \
                .add_piglets_today_quantity() \
                .add_piglets_quantity_at_date_start() \
                .add_born_alive() \
                .add_piglets_padej_qnty() \
                .add_piglets_prirezka_qnty() \
                .add_piglets_vinuzhd_qnty() \
                .add_piglets_spec_qnty() \
                .add_piglets_quantity_at_date_end() \
                .add_piglets_qnty_in_transactions() \
                .add_piglets_spec_total_weight() \
                .add_priplod_by_sow() \

    serializer_class = ReportDateSerializer
    filter_class = ReportDateFilter
    pagination_class = CustomPagination

    # def list(self, request):
    #     page = self.paginate_queryset(self.queryset)

    #     if page is not None:
    #         data = ReportDateSerializer(page, many=True).data
    #         total_info = 'Hello'
    #         return self.get_paginated_response(data, total_info)

    #     serializer = ReportDateSerializer(self.queryset, many=True)
    #     return Response(serializer.data)