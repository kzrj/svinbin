# -*- coding: utf-8 -*-
from datetime import timedelta, date

from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework import status, viewsets, pagination, views
from rest_framework.response import Response
from rest_framework.decorators import action

from tours.filters import TourFilter

from tours.models import Tour
from piglets.models import Piglets
from sows_events.models	import SowFarrow
from reports.models import ReportDate
from locations.models import Location

from reports.serializers import ReportDateSerializer, ReportTourSerializer
from reports.filters import ReportDateFilter


class TourReportViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all() \
                .order_by('-year','-week_number', ) \
                .add_sow_data() \
                .add_farrow_data() \
                .add_count_tour_sow() \
                .add_weight_date() \
                .add_week_weight() \
                .add_week_weight_ws8_v2() \
                .add_culling_data_by_week_tour() \
                .add_piglets_count_by_ws_week_tour() \
                .add_gilts_count_by_ws_week_tour() \
                .add_count_transfer_to_7_5() \
                .add_culling_percentage()

    serializer_class = ReportTourSerializer
    filter_class = TourFilter


# class CustomPagination(pagination.PageNumberPagination):
#     def get_paginated_response(self, data):
#         return Response({
#             'links': {
#                 'next': self.get_next_link(),
#                 'previous': self.get_previous_link()
#             },
#             'count': self.page.paginator.count,
#             'total_info': data['total_info'],
#             'pigs_count': data['pigs_count'],
#             'results': data['results'],
#         })


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
    # pagination_class = CustomPagination

    def list(self, request):
        queryset = self.filter_queryset(self.queryset)

        serializer = ReportDateSerializer(queryset, many=True)

        total_data = queryset.dir_rep_aggregate_total_data()

        last_date = queryset.order_by('-date').first()
        pigs_count = 0
        if last_date:
            pigs_count = last_date.sows_quantity_at_date_end + last_date.piglets_qnty_start_end

        data = {'results': serializer.data, 'total_info': total_data, 'pigs_count': pigs_count}

        return Response({
            'total_info': data['total_info'],
            'pigs_count': data['pigs_count'],
            'results': data['results'],
        })


class ReportCountPigsView(views.APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        data = Location.objects.gen_sections_pigs_count_dict()
        return Response(data)