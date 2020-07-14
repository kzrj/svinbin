# -*- coding: utf-8 -*-
from django.db.models import CharField, Value
from django.utils import timezone
from django.http import HttpResponse

from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action

from core.utils import export_to_excel_ws3

from tours.filters import TourFilter

from tours.models import Tour
from reports.models import ReportDate, gen_operations_dict, gen_megadict
from locations.models import Location
from sows_events.models import ( Semination, Ultrasound, AbortionSow, CullingSow, MarkAsNurse, MarkAsGilt )
from piglets_events.models import CullingPiglets, WeighingPiglets
from transactions.models import SowTransaction, PigletsTransaction
from sows.models import Sow
from piglets.models import Piglets

from reports.serializers import ReportDateSerializer, ReportTourSerializer, ReportDateWs3Serializer
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
                .add_culling_percentage() \
                .order_by('-year','-week_number', ) \
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

    @action(methods=['get'], detail=False)
    def ws3_report(self, request):
        ws3_locs = Location.objects.all().get_workshop_location_by_number(workshop_number=3)
        bool(ws3_locs)
        queryset = ReportDate.objects.all()\
                            .add_ws3_sow_cullings_data(ws_locs=ws3_locs) \
                            .add_ws3_sow_trs_data(ws_locs=ws3_locs) \
                            .add_ws3_sow_farrow_data() \
                            .add_ws3_count_piglets_start_day(ws_locs=ws3_locs) \
                            .add_ws3_piglets_trs_out_aka_weighing() \
                            .add_ws3_piglets_cullings(ws_locs=ws3_locs)
        queryset = self.filter_queryset(queryset)
        total_data = queryset.ws3_aggregate_total()

        serializer = ReportDateWs3Serializer(queryset, many=True)

        data = dict()
        data['results'] = serializer.data
        data['total_info'] = total_data

        export_to_excel_ws3(data=data)
        
        return Response(data)

    @action(methods=['get'], detail=False)
    def ws_report(self, request):
        ws_number = int(request.GET.get('ws_number', 0))

        ws_locs = Location.objects.all().get_workshop_location_by_number(workshop_number=ws_number)
        bool(ws_locs)
        queryset = ReportDate.objects.all()\
                            .add_ws_count_piglets_start_day(ws_locs=ws_locs) \
                            .add_ws_weighing_in(ws_number=ws_number) \
                            .add_ws_weighing_out(ws_number=ws_number) \
                            .add_ws_piglets_culling_data(ws_locs=ws_locs) \
                            .add_ws_piglets_trs_in_out(ws_locs=ws_locs) \

        queryset = self.filter_queryset(queryset)
        total_data = queryset.ws_aggregate_total()
        

        serializer = ReportDateSerializer(queryset, many=True)

        data = dict()
        data['results'] = serializer.data
        data['total_info'] = total_data

        # export_to_excel_ws3(data=data)
        
        return Response(data)

    @action(methods=['get'], detail=False)
    def ws_report_count(self, request):
        ws_number = request.GET.get('ws_number', None)
        data = dict()

        if ws_number == 3 or ws_number == '3':
            ws3_locs = Location.objects.all().get_workshop_location_by_number(workshop_number=3)
            bool(ws3_locs)
            ws3_sows_sup_count = Sow.objects.filter(location__in=ws3_locs, status__title='Супорос 35').count()
            ws3_sows_pods_count = Sow.objects.filter(location__in=ws3_locs,
                status__title__in=['Опоросилась', 'Отъем', 'Кормилица']).count()
            ws3_sows_nurse_count = Sow.objects.filter(location__in=ws3_locs,
                status__title__in=['Кормилица']).count()
            ws3_piglets_count = Piglets.objects.filter(location__in=ws3_locs).get_total_quantity()
            ws3_gilts_count = Piglets.objects.filter(location__in=ws3_locs).get_total_gilts_quantity()
            
            data['ws_number'] = 3
            data['ws3_sows_sup_count'] = ws3_sows_sup_count
            data['ws3_sows_pods_count'] = ws3_sows_pods_count
            data['ws3_sows_nurse_count'] = ws3_sows_nurse_count
            data['ws_piglets_count'] = ws3_piglets_count
            data['ws3_gilts_count'] = ws3_gilts_count

        return Response(data)

    @action(methods=['get'], detail=False)
    def get_ws3_report_excel(self, request):      
        file = open('../data/ws3_output.xlsx', 'rb')
        response = HttpResponse(file, content_type="application/file")
        response['Content-Disposition'] = 'attachment; filename={}'.format('ws3_report.xlsx')
        return response


class ReportCountPigsView(views.APIView):
    def get(self, request, format=None):
        data = Location.objects.all().gen_sections_pigs_count_dict() 
        return Response(data)


class OperationsDataView(views.APIView):
    pagination = LimitOffsetPagination()

    def post(self, request):
        operations_data = gen_operations_dict()
        megadict = gen_megadict(request.data)
        return Response(megadict)
        # return Response(self.pagination.get_paginated_response(data=megalist))