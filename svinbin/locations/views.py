# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testing
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing

from locations.models import Location, Section
from locations import serializers
from locations.filters import LocationFilter, SectionFilter
from core.permissions import ReadOrAdminOnlyPermissions


class CreateWorkshopsView(APIView):
    def get(self, request, format=None):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        staff_testing.create_svinbin_users()
        sows_testing.create_boars()
        sows_events_testing.create_types()

        return Response({'msg': 'success'})


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = serializers.LocationCellSerializer
    filter_class = LocationFilter
    permission_classes = [ReadOrAdminOnlyPermissions]

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
                        'piglets__metatour__week_tour',)
            )

        if request.GET.get('cells_piglets'):
            serializer = serializers.LocationPigletsCellSerializer
            queryset = self.filter_queryset(
                self.get_queryset() \
                    .select_related(
                        'pigletsGroupCell__section',
                        'sowAndPigletsCell__section',
                        ) \
                    .prefetch_related(
                        'piglets__metatour__week_tour',)
            )

        if request.GET.get('cells_piglets_vet'):
            serializer = serializers.LocationPigletsVetCellSerializer
            queryset = self.filter_queryset(
                self.get_queryset() \
                    .select_related(
                        'pigletsGroupCell__section',
                        'sowAndPigletsCell__section',
                        ) \
                    .prefetch_related(
                        'piglets__metatour__week_tour',
                        'piglets__pigletsvetevent_set__recipe',
                        )
            )

        if request.GET.get('cells_sows'):
            serializer = serializers.LocationSowCellSerializer
            queryset = self.filter_queryset(
                self.get_queryset() \
                    .filter(sowAndPigletsCell__isnull=False) \
                    .select_related(
                        'sowAndPigletsCell__section',
                        ) \
                    .prefetch_related(
                        'sow_set__tour',
                        'sow_set__status')
                )

        if request.GET.get('sections'):
            serializer = serializers.LocationSectionSerializer
            queryset = self.filter_queryset(
                self.get_queryset()\
                    .select_related('section__workshop').add_pigs_count_by_sections()
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def ws3_and_sections(self, request):
        today = datetime.today()
        
        ws3 = Location.objects.filter(workshop__number=3) \
                .select_related('workshop') \
                .add_sows_count_by_workshop() \
                .add_pigs_count_by_workshop() \
                .add_pigs_count_by_workshop3_by_age(date=today) \
                .first()

        section_locs = Location.objects.filter(section__workshop__number=3,
             section__isnull=False) \
                .select_related('section') \
                .add_sows_count_by_sections() \
                .add_pigs_count_by_sections() \
                .add_pigs_count_by_ws3_sections_by_age(date=today)

        data = dict()
        data['ws'] = {
            'sows_count': ws3.sows_count, 
            'sows_sup_count': ws3.sows_sup_count,
            'pigs_count': ws3.pigs_count,
            'count_piglets_0_7': ws3.count_piglets_0_7,
            'count_piglets_8_14': ws3.count_piglets_8_14,
            'count_piglets_15_21': ws3.count_piglets_15_21,
            'count_piglets_22_28': ws3.count_piglets_22_28,
            'count_piglets_28_plus': ws3.count_piglets_28_plus,
            }

        data['sections'] = list()
        for section in section_locs:
            data['sections'].append({
                'section_number': section.section.number,
                'section_id': section.section.pk,
                'sows_count': section.sows_count,
                'sows_sup_count': section.sows_sup_count,
                'piglets_count': section.pigs_count,
                'count_piglets_0_7': section.count_piglets_0_7,
                'count_piglets_8_14': section.count_piglets_8_14,
                'count_piglets_15_21': section.count_piglets_15_21,
                'count_piglets_22_28': section.count_piglets_22_28,
                'count_piglets_28_plus': section.count_piglets_28_plus,
            })

        return Response(data)


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all().select_related('location')
    serializer_class = serializers.SectionSerializer
    filter_class = SectionFilter
    permission_classes = [ReadOrAdminOnlyPermissions]