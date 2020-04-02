# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from piglets.models import Piglets

class ReportsViewSet(viewsets.ViewSet):
    @action(detail=False)
    def report_workshop(self, request):
    	# Piglets.objects.with_tour()

    	# all tours in ws
    	# tours.objects.filter(metarecords__metatour__piglets__in)

    	return Response({'report': 'report'})