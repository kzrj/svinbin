# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from piglets.models import Piglets
from sows_events.models	import SowFarrow


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
