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
                .add_count_tour_sow() \
                .add_weight_date() \
                .add_week_weight() \
                .add_week_weight_ws8() \
                .add_culling_data_by_week_tour()

    serializer_class = ReportTourSerializer
    filter_class = TourFilter