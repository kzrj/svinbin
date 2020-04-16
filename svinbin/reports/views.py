# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from tours.filters import TourFilter

from tours.models import Tour
from piglets.models import Piglets
from sows_events.models	import SowFarrow

from reports.serializers import ReportTourSerializer


class ReportsViewSet(viewsets.ViewSet):
    @action(detail=False)
    def report_workshop(self, request):
    	# Piglets.objects.with_tour()

    	# all tours in ws
    	# tours = tours.objects.filter(metarecords__metatour__piglets__in=piglets_in_ws).distinct()

    	return Response({'report': 'report'})

    @action(detail=False)
    def report_tours(self, request):
    	# born
    	SowFarrow.objects.filter(tour).count_piglets()

    	Piglets.objects.with_tour_not_mixed(tour)
    	Piglets.objects.with_tour_mixed(tour)




    	return Response({'report_tours': 'report'})


class TourReportViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all() \
                .add_sow_data() \
                .add_farrow_data() \
                .add_current_not_mixed_piglets_quantity() \
                .add_current_mixed_piglets_quantity() \
                .add_weight_data_not_mixed() \
                .add_weight_data_mixed() \
                .add_avg_weight_data() \
                .add_culling_weight_not_mixed_piglets() \
                .add_culling_qnty_not_mixed_piglets() \
                .add_culling_avg_weight_not_mixed_piglets() \
                .add_culling_percentage_not_mixed_piglets() \
                .add_weight_date() \
                # .add_count_tour_sow() \
                # .add_culling_data_by_ws() \
                # .add_current_piglets_age() \
                # .add_age_at_weight_date() \

    serializer_class = ReportTourSerializer
    filter_class = TourFilter

    # def list(self, request):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.serializer_class

    #     if request.GET.get('cells'):
    #         serializer = serializers.LocationCellSerializer
    #         queryset = self.filter_queryset(
    #             self.get_queryset() \
    #                 .select_related(
    #                     'pigletsGroupCell__section',
    #                     'sowAndPigletsCell__section',
    #                     'sowSingleCell__section',
    #                     'sowGroupCell__section',
    #                     ) \
    #                 .prefetch_related(
    #                     'sow_set__tour',
    #                     'sow_set__status',
    #                     'piglets__metatour__records__tour',)
    #         )

    #     if request.GET.get('sections'):
    #         serializer = serializers.LocationSectionSerializer
    #         queryset = self.filter_queryset(
    #             self.get_queryset()\
    #                 .select_related('section__workshop').get_with_count_piglets_in_section()
    #         )

    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = serializer(queryset, many=True)
    #     return Response(serializer.data)