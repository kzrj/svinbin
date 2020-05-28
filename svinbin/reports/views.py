# -*- coding: utf-8 -*-
from django.db.models import CharField, Value
from django.utils import timezone

from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from tours.filters import TourFilter

from tours.models import Tour
from reports.models import ReportDate, gen_operations_dict, gen_megalist
from locations.models import Location
from sows_events.models import ( Semination, Ultrasound, AbortionSow, CullingSow, MarkAsNurse, MarkAsGilt )
from piglets_events.models import CullingPiglets, WeighingPiglets
from transactions.models import SowTransaction, PigletsTransaction

from reports.serializers import ReportDateSerializer, ReportTourSerializer
from reports.filters import ReportDateFilter


class TourReportViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all() \
                .add_sow_data() \
                .add_farrow_data() \
                .add_count_tour_sow() \
                .add_week_weight() \
                .add_week_weight_ws8_v2() \
                .add_culling_data_by_week_tour() \
                .add_count_transfer_to_7_5() \
                # .add_culling_percentage() \
                # .order_by('-year','-week_number', ) \
                # .filter(year__gte=2020)

    serializer_class = ReportTourSerializer
    filter_class = TourFilter


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

    def list(self, request):
        queryset = self.filter_queryset(self.queryset)

        serializer = ReportDateSerializer(queryset, many=True)

        total_data = queryset.dir_rep_aggregate_total_data()

        last_date = queryset.order_by('-date').first()
        pigs_count = 0
        if last_date:
            sows_quantity_at_date_end = last_date.sows_quantity_at_date_end \
                if last_date.sows_quantity_at_date_end else 0
            piglets_qnty_start_end = last_date.piglets_qnty_start_end \
                if last_date.piglets_qnty_start_end else 0
            pigs_count = sows_quantity_at_date_end + piglets_qnty_start_end

        data = {'results': serializer.data, 'total_info': total_data, 'pigs_count': pigs_count}

        return Response({
            'total_info': data['total_info'],
            'pigs_count': data['pigs_count'],
            'results': data['results'],
        })


class ReportCountPigsView(views.APIView):
    def get(self, request, format=None):
        data = Location.objects.all().gen_sections_pigs_count_dict()
        return Response(data)


class OperationsDataView(views.APIView):
    pagination = LimitOffsetPagination()

    def post(self, request):
        operations_data = gen_operations_dict()
        megalist = gen_megalist(request.data)
        return Response(megalist)
        # return Response(self.pagination.get_paginated_response(data=megalist))