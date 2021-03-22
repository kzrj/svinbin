# -*- coding: utf-8 -*-
import datetime
from django.db.models import CharField, Value
from django.utils import timezone
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action

from core.utils import export_to_excel_ws3, export_to_excel_ws

from tours.filters import TourFilter

from tours.models import Tour
from reports.models import ReportDate, gen_operations_dict, gen_megadict
from locations.models import Location
from sows_events.models import ( Semination, Ultrasound, AbortionSow, CullingSow, MarkAsNurse, MarkAsGilt,
    CullingBoar)
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
            .add_remont_to_sows() \
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

    @action(methods=['get'], detail=False)
    def by_ws(self, request):
        data = dict()
        return Response(data)


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
                            .add_ws_count_piglets_start_day(ws_locs=ws_locs, ws_numbers=[ws_number]) \
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
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('start_date', None)
        if end_date and start_date:
            data = dict()
            ws3_locs = Location.objects.all().get_workshop_location_by_number(ws_number=3)
            ws48_locs = Location.objects.all().get_workshop_location_by_number(ws_number=4) | \
                        Location.objects.get_workshop_location_by_number(ws_number=8)

            ws567_locs = Location.objects.all().get_workshop_location_by_number(ws_number=5) | \
                        Location.objects.all().get_workshop_location_by_number(ws_number=6) | \
                        Location.objects.all().get_workshop_location_by_number(ws_number=7)

            # count start date, end date
            start_date_sows = Sow.objects.get_sows_at_date(date=start_date) \
                                         .add_group_at_date(date=start_date) \
                                         .add_group_at_date_count('Ремонтная', 'rem') \
                                         .add_group_at_date_count('Проверяемая', 'prov') \
                                         .add_group_at_date_count('С опоросом', 'osn').first()
            data['start_sows_osn_count'] = start_date_sows.count_group_osn
            data['start_sows_prov_count'] = start_date_sows.count_group_prov
            data['start_sows_rem_count'] = start_date_sows.count_group_rem

            end_date_sows = Sow.objects.get_sows_at_date(date=end_date) \
                                         .add_group_at_date(date=end_date) \
                                         .add_group_at_date_count('Ремонтная', 'rem') \
                                         .add_group_at_date_count('Проверяемая', 'prov') \
                                         .add_group_at_date_count('С опоросом', 'osn').first()
            data['end_sows_osn_count'] = end_date_sows.count_group_osn
            data['end_sows_prov_count'] = end_date_sows.count_group_prov
            data['end_sows_rem_count'] = end_date_sows.count_group_rem
                                         
            dates = ReportDate.objects.filter(Q(date=start_date) | Q(date=end_date)) \
                        .add_count_boars() \
                        .add_ws3_count_piglets_start_day(ws_locs=ws3_locs) \
                        .add_ws_count_piglets_start_day(ws_locs=ws48_locs, ws_numbers=[4, 8]) \
                        .add_ws_count_piglets_start_day(ws_locs=ws567_locs, ws_numbers=[5, 6, 7])

            data['start_ws3_piglets_count'] = dates[0].count_piglets_at_start
            data['start_ws48_piglets_count'] = dates[0].ws48_count_piglets_at_start
            data['start_ws567_piglets_count'] = dates[0].ws567_count_piglets_at_start
            data['start_boars_count'] = dates[0].count_boars
            data['end_ws3_piglets_count'] = dates[1].count_piglets_at_start
            data['end_ws48_piglets_count'] = dates[1].ws48_count_piglets_at_start
            data['end_ws567_piglets_count'] = dates[1].ws567_count_piglets_at_start
            data['end_boars_count'] = dates[1].count_boars

            # aggregates. calc between start and end
            # 1. prov to osn
            # 2. rem to prov
            data['sow_group_transfer'] = SowGroupRecord.objects.all().count_group_tranfer_in_daterange(
                start_date=start_date, end_date=end_date)
            # 3. to rem
            data['sow_group_transfer']['to_rem'] = PigletsToSowsEvent.objects.filter(
                date__date__gte=start_date, date__date__lt=end_date).aggregate(qnty=Sum('quantity'))['qnty']

            # 4. total born alive
            data['total_born_alive'] = SowFarrow.objects.filter(date__date__gte=start_date,
                date__date__lt=end_date).aggregate(qnty=Sum('alive_quantity'))['qnty']

            # 5. 3\4 8\otkorm weighing
            data['count_doros_otkorm_in_out'] = WeighingPiglets.objects \
                .filter(date__date__gte=start_date, date__date__lt=end_date) \
                .count_doros_otkorm_in_out()

            # 6. culls sows + rem
            data['culls_sows'] = CullingSow.objects.filter(date__date__gte=start_date,
                date__date__lt=end_date).count_by_groups()

            # 7. culls piglets by ws
            data['ws3_culls'] = CullingPiglets.objects.filter(date__date__gte=start_date,
                date__date__lt=end_date).count_at_loc(locs=ws3_locs, label='_ws3')
            data['ws48_culls'] = CullingPiglets.objects.filter(date__date__gte=start_date,
                date__date__lt=end_date).count_at_loc(locs=ws48_locs, label='_ws48')
            data['ws567_culls'] = CullingPiglets.objects.filter(date__date__gte=start_date,
                date__date__lt=end_date).count_at_loc(locs=ws567_locs, label='_ws567')

            # 8. culls boars
            data['ws567_culls'] = CullingBoar.objects.filter(date__date__gte=start_date,
                date__date__lt=end_date).count_by_groups()

            return Response(data)
        else:
            return Response({'message': 'Неверные даты.'}, status=status.HTTP_400_BAD_REQUEST)

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
    @staticmethod
    def gen_places(ws_number):
        places = ''
        if ws_number == 3:
            places = ['3/4']
        if ws_number == 4:
            places = ['3/4', '4/8']
        if ws_number == 8:
            places = ['4/8', '8/5', '8/6', '8/7']
        if ws_number == 5:
            places = ['8/5',]
        if ws_number == 6:
            places = ['8/6',]
        if ws_number == 7:
            places = ['8/7',]
        return places

    @action(methods=['post'], detail=False)
    def ws_population_and_tours(self, request):
        ws_number = int(request.data.get('ws_number', 4))
        age_intervals = request.data.get('age_intervals', [])
        today = datetime.datetime.today()

        ws = Location.objects.filter(workshop__number=ws_number) \
            .add_pigs_count_by_workshop() \
            .add_pigs_count_by_workshop_by_age(date=today, age_intervals=age_intervals)
        sections = Location.objects.filter(section__workshop__number=ws_number) \
            .add_pigs_count_by_sections() \
            .add_pigs_count_by_ws_sections_by_age(date=today, age_intervals=age_intervals) \
            .add_section_fullness()

        places = self.gen_places(ws_number=ws_number)
        tours = Tour.objects.filter(piglets_weights__place__in=places).distinct()

        if ws_number in [5, 6, 7]:
            tours = tours.add_remont_to_sows(ws_numbers=[ws_number,])

        tours = tours.add_week_weight(places=places)

        if ws_number == 8:
            tours = tours.add_week_weight_ws8_v2()
    
        tours = tours.add_culling_data_by_week_tour(ws_numbers=[ws_number, ]) \
                .add_culling_percentage(ws_numbers=[ws_number,]) \
                .add_prives(ws_numbers=[ws_number, ]) \
                .add_prives_na_1g(ws_numbers=[ws_number, ]) \
                .order_by('-year','-week_number')[:15]

        data = {'population': {}, 'tours': {}}
        data['population']['sections'] = LocationSectionPopulationSerializer(sections, many=True).data
        data['population']['ws'] = LocationWSPopulationSerializer(ws, many=True).data[0]
        data['tours'] = ReportTourSerializer(tours, many=True).data

        return Response(data)

    @action(methods=['post'], detail=False)
    def main_page_population(self, request):
        today = datetime.datetime.today()
        ws12 = Location.objects.filter(workshop__number__in=[1,2]).add_sows_count_by_workshop()

        ws3 = Location.objects.filter(workshop__number=3) \
                .add_sows_count_by_workshop() \
                .add_pigs_count_by_workshop(date=today, 
                    age_intervals=[[0, 7], [8, 14], [15, 21], [22, 28], [28, None]])

        ws4 = Location.objects.filter(workshop__number=4) \
                .add_pigs_count_by_workshop(date=today, 
                    age_intervals=[[0, 7], [8, 14], [15, 21], [22, 28], [28, None]])

        ws5 = Location.objects.filter(workshop__number=5) \
                .add_pigs_count_by_workshop(date=today, 
                    age_intervals=[[0, 7], [8, 14], [15, 21], [22, 28], [28, None]])

        ws6 = Location.objects.filter(workshop__number=6) \
                .add_pigs_count_by_workshop(date=today, 
                    age_intervals=[[0, 7], [8, 14], [15, 21], [22, 28], [28, None]])

        ws7 = Location.objects.filter(workshop__number=7) \
                .add_pigs_count_by_workshop(date=today, 
                    age_intervals=[[0, 7], [8, 14], [15, 21], [22, 28], [28, None]])

        ws8 = Location.objects.filter(workshop__number=8) \
                .add_pigs_count_by_workshop(date=today, 
                    age_intervals=[[0, 7], [8, 14], [15, 21], [22, 28], [28, None]])

        wss = ws12 | ws3 | ws4 | ws8 | ws5 | ws6 | ws7

        wss = wss.add_pigs_count_by_workshop()

        # to do:
        # final data
        # add cullings today by ws
