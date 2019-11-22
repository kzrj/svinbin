# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testing
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing

from locations.models import PigletsGroupCell, Location, Section
from locations import serializers
from locations.filters import LocationFilter, SectionFilter


class CreateWorkshopsView(APIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        staff_testing.create_test_users()
        sows_testing.create_boars()
        sows_events_testing.create_types()

        return Response({'msg': 'success'})


# class PigletsGroupCellViewSet(viewsets.ModelViewSet):
#     queryset = PigletsGroupCell.objects.all()
#     serializer_class = serializers.PigletsGroupCellSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.prefetch_related('sow_set', 'newbornpigletsgroup_set',
        'nomadpigletsgroup_set', 'gilt_set').all()
    serializer_class = serializers.LocationSerializer
    filter_class = LocationFilter


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = serializers.SectionSerializer
    filter_class = SectionFilter