# -*- coding: utf-8 -*-
import datetime
from django.db.models import CharField, Value
from django.utils import timezone
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action

from core.utils import export_to_excel_ws3, export_to_excel_ws

from tours.filters import TourFilter

from tours.models import Tour
from reports.models import ReportDate, gen_operations_dict, gen_megadict
from locations.models import Location
from sows_events.models import ( Semination, Ultrasound, AbortionSow, CullingSow, MarkAsNurse, MarkAsGilt )
from piglets_events.models import CullingPiglets, WeighingPiglets
from transactions.models import SowTransaction, PigletsTransaction
from sows.models import Sow
from piglets.models import Piglets

from reports.serializers import ReportDateSerializer, ReportTourSerializer, ReportDateWs3Serializer, \
    StartDateEndDateSerializer, TotalWeightsSerializer
from piglets_events.serializers import WeighingPigletsReadSerializer, CullingPigletsReadSerializer
from tours.serializers import TourSerializer
from sows.serializers import SowDowntimeSerializer
from locations.serializers import LocationWSPopulationSerializer, LocationSectionPopulationSerializer

from reports.filters import ReportDateFilter
from core.permissions import ReadOrAdminOnlyPermissions


class TourReportViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all() 
    serializer_class = ReportTourSerializer
    filter_class = TourFilter
    permission_classes = [ReadOrAdminOnlyPermissions]

    def list(self, request):
        queryset = self.filter_queryset(
            self.queryset \
            .add_remont_trs_out() \
            .add_farrow_data() \
            .add_sow_data() \
            .add_farrow_percentage() \
            .add_week_weight() \
            .add_week_weight_ws8_v2() \
            .add_culling_data_by_week_tour() \
            .add_culling_percentage() \
            .add_prives() \
            .add_prives_na_1g() \
            .order_by('-year','-week_number', ) \
            )
        serializer = ReportTourSerializer(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ReportTourSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

        return super().list(request)


class TourReportV2ViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all() \
               .add_weighing_first_dates()

    serializer_class = ReportTourSerializer
    filter_class = TourFilter
    permission_classes = [ReadOrAdminOnlyPermissions]

    @action(methods=['get'], detail=True)
    def weights_data(self, request, pk=None, serializer_class=None):
        tour = self.get_object()
        data = dict()
        for place in ['3/4', '4/8', '8/5', '8/6', '8/7']:
            place_formatted = place.replace('/', '_')
            data[place] = dict()
            qs, total = tour.piglets_weights.all().get_tour_data_by_place(tour=tour, place=place)
            data[place]['list'] = WeighingPigletsReadSerializer(qs, many=True).data
            data[place]['total'] = TotalWeightsSerializer(total).data

        for ws_number in [5, 6, 7]:
            qs, total = tour.piglets_culling.get_by_tour_and_ws_number(tour=tour, ws_number=ws_number)
            data[f'spec_{str(ws_number)}'] = dict()
            data[f'spec_{str(ws_number)}']['list'] = CullingPigletsReadSerializer(qs, many=True).data
            data[f'spec_{str(ws_number)}']['total'] = TotalWeightsSerializer(total).data

        data['farrow_data'] = tour.sowfarrow_set.count_piglets()
        data['tour'] = TourSerializer(tour).data

        return Response(data)


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
    permission_classes = [ReadOrAdminOnlyPermissions]

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
    def director(self, request):
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
                            .add_ws_count_piglets_start_day(ws_locs=ws_locs, ws_number=ws_number) \
                            .add_ws_weighing_in(ws_number=ws_number) \
                            .add_ws_piglets_trs_in_out(ws_locs=ws_locs) \
                            .add_ws_weighing_out(ws_number=ws_number) \
                            .add_ws_piglets_culling_data(ws_locs=ws_locs) \

        queryset = self.filter_queryset(queryset)
        total_data = queryset.ws_aggregate_total()

        serializer = ReportDateSerializer(queryset, many=True)

        data = dict()
        data['results'] = serializer.data
        data['total_info'] = total_data

        export_to_excel_ws(data=data, ws_number=ws_number)
        
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

    @action(methods=['get'], detail=False)
    def get_ws_report_excel(self, request):
        ws_number = request.GET.get('ws_number', None)    
        file = open(f'../data/ws{ws_number}_output.xlsx', 'rb')
        response = HttpResponse(file, content_type="application/file")
        response['Content-Disposition'] = 'attachment; filename={}'.format(f'ws{ws_number}_report.xlsx')
        return response

    @action(methods=['get'], detail=False, serializer_class=StartDateEndDateSerializer)
    def ws_24f_report(self, request):
        serializer = StartDateEndDateSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            start_date_sows = Sow.objects.get_sows_at_date(date=start_date) \
                                         .add_group_at_date(date=start_date) \
                                         .add_group_at_date_count()

            end_date = serializer.validated_data['end_date']
            end_date_sows = Sow.objects.get_sows_at_date(date=end_date) \
                                         .add_group_at_date(date=end_date) \
                                         .add_group_at_date_count()

            # todo:
            # count boars start end
            # count piglets start end
            
            # count cullings by group, boar, piglets
            # count transactions by group, boar, piglets

            # rest

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, serializer_class=StartDateEndDateSerializer)
    def ws12_report(self, request):
        ws_number = request.GET.get('ws_number', 1)
        fix_number = 0
        if int(ws_number) == 1:
            fix_number = 1639
        else:
            fix_number = 335

        ws_locs = Location.objects.all().get_workshop_location_by_number(workshop_number=ws_number)
        bool(ws_locs)
        
        queryset = ReportDate.objects.all()\
                            .add_count_sows_ws12(ws_number=ws_number, fix_number=fix_number) \
                            .add_count_boars() \
                            .add_ws12_sow_cullings_data(ws_locs=ws_locs, ws_number=ws_number) \
                            .add_culling_boar_data() \
                            .add_ws12_sow_trs_data() 

        queryset = self.filter_queryset(queryset)
        total_data = queryset.ws12_aggregate_total(ws_number=ws_number)

        serializer = ReportDateSerializer(queryset, many=True)

        data = dict()
        data['results'] = serializer.data
        data['total_info'] = total_data

        return Response(data)


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


class ReportSowsDowntimeByStatusesView(viewsets.ViewSet):
    @staticmethod
    def gen_data_dict(days, statuses):
        data = dict()    
        sows_count, downtime_sows_qs = Sow.objects.all().sows_by_statuses_count_and_downtime_qs(
            days_limit=days, statuses=statuses)
        data['count_all'] = sows_count
        data['downtime_sows'] = SowDowntimeSerializer(downtime_sows_qs, many=True).data

        return data

    def list(self, request):
        downtime_wait_days  = int(request.GET.get('downtime_wait_days', 40))
        downtime_sem_days   = int(request.GET.get('downtime_sem_days', 28))
        downtime_sup28_days = int(request.GET.get('downtime_sup28_days', 7))
        downtime_sup35_days = int(request.GET.get('downtime_sup35_days', 65))
        downtime_farr_days  = int(request.GET.get('downtime_farr_days', 30))
        downtime_nurse_days = int(request.GET.get('downtime_nurse_days', 21))

        data = {'wait': dict(), 'sem': dict(), 'sup28': dict(), 'sup35': dict(),
            'farr': dict(), 'nurse':dict() }

        data['wait'] = self.gen_data_dict(days=downtime_wait_days, 
            statuses=['Ремонтная', "Ожидает осеменения", "Прохолост", "Аборт"])
        data['sem'] = self.gen_data_dict(days=downtime_sem_days, statuses=['Осеменена 2'])
        data['sup28'] = self.gen_data_dict(days=downtime_sup28_days, statuses=['Супорос 28'])
        data['sup35'] = self.gen_data_dict(days=downtime_sup35_days, statuses=['Супорос 35'])
        data['farr'] = self.gen_data_dict(days=downtime_farr_days, statuses=['Опоросилась', 'Отъем'])
        data['nurse'] = self.gen_data_dict(days=downtime_nurse_days, statuses=['Кормилица'])

        return Response(data)


class ReportWSInfoView(viewsets.ViewSet):
    @action(methods=['post'], detail=False)
    def ws_population_and_tours(self, request):
        ws_number = request.data.get('ws_number', 4)
        age_intervals = request.data.get('age_intervals', [])
        today = datetime.datetime.today()

        ws = Location.objects.filter(workshop__number=ws_number) \
            .add_pigs_count_by_workshop() \
            .add_pigs_count_by_workshop_by_age(date=today, age_intervals=age_intervals)
        sections = Location.objects.filter(section__workshop__number=ws_number) \
            .add_pigs_count_by_sections() \
            .add_pigs_count_by_ws_sections_by_age(date=today, age_intervals=age_intervals)

        data = {'population': {}, 'tours': {}}
        data['population']['sections'] = LocationSectionPopulationSerializer(sections, many=True).data
        data['population']['ws'] = LocationWSPopulationSerializer(ws, many=True).data[0]

        return Response(data)


