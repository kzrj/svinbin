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
        # staff_testing.create_test_users()
        staff_testing.create_svinbin_users()
        sows_testing.create_boars()
        sows_events_testing.create_types()

        return Response({'msg': 'success'})


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = serializers.LocationSerializer
    filter_class = LocationFilter

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class

        if request.GET.get('cells'):
            serializer = serializers.LocationCellSerializer
            queryset = self.filter_queryset(
                self.get_queryset() \
                    .select_related(
                        'pigletsGroupCell__section',
                        'sowAndPigletsCell__section',
                        'sowSingleCell__section',
                        'sowGroupCell__section',
                        ) \
                    .prefetch_related(
                        'sow_set__tour',
                        'sow_set__status',
                        'piglets__metatour__records__tour',)
            )

        if request.GET.get('sections'):
            serializer = serializers.LocationSectionSerializer
            queryset = self.filter_queryset(
                self.get_queryset()\
                    .select_related('section__workshop').get_with_count_piglets_in_section()
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer(queryset, many=True)
        return Response(serializer.data)


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all().select_related('location')
    serializer_class = serializers.SectionSerializer
    filter_class = SectionFilter