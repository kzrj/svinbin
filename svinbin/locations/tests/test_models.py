# -*- coding: utf-8 -*-
from django.test import TestCase, TransactionTestCase
from django.db import models

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing
import sows_events.utils as sows_events_testing

from locations.models import (
    Location, WorkShop, Section, 
    SowSingleCell, PigletsGroupCell, 
    SowGroupCell, SowAndPigletsCell
    )
from sows_events.models import SowFarrow

from locations.serializers import (
    LocationSerializer, LocationCellSerializer, LocationSectionSerializer
    )


class LocationModelManagerQuerysetTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        sows_events_testing.create_types()

        location1 = Location.objects.filter(sowAndPigletsCell__number=1).first()
        sow1 = sows_testing.create_sow_with_semination_usound(location=location1, week=1)
        location2 = Location.objects.filter(sowAndPigletsCell__number=2).first()
        sow2 = sows_testing.create_sow_with_semination_usound(location=location2, week=1)
        location3 = Location.objects.filter(sowAndPigletsCell__number=3).first()
        sow3 = sows_testing.create_sow_with_semination_usound(location=location3, week=2)
        location4 = Location.objects.filter(sowAndPigletsCell__number=4).first()
        sow4 = sows_testing.create_sow_with_semination_usound(location=location4, week=2)
        location5 = Location.objects.filter(sowAndPigletsCell__number=5).first()
        sow5 = sows_testing.create_sow_with_semination_usound(location=location5, week=3)
        location6 = Location.objects.filter(sowAndPigletsCell__number=6).first()
        sow6 = sows_testing.create_sow_with_semination_usound(location=location6, week=4)
        location7 = Location.objects.filter(sowAndPigletsCell__number=7).first()
        sow7 = sows_testing.create_sow_with_semination_usound(location=location7, week=5)

        SowFarrow.objects.create_sow_farrow(sow=sow1, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow2, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow3, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow4, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow5, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow6, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow7, alive_quantity=10)

    # def test_queryset_with_all_related(self):
    #     with self.assertNumQueries(3):
    #         data = Location.objects.all()\
    #             .select_related('section', 'workshop', 'pigletsGroupCell', 'sowAndPigletsCell' ) \
    #             .prefetch_related('sow_set', 'piglets__metatour__records__tour',)
    #         print(data)

    #     with self.assertNumQueries(5):
    #         for location in data:
    #             for piglet in location.piglets.all():
    #                 print(piglet.metatour_repr)

    def test_location_cell_serializer_queries(self):
        with self.assertNumQueries(8):
            data = Location.objects.all() \
                .select_related(
                    'pigletsGroupCell__section',
                    'sowAndPigletsCell__section',
                    'sowSingleCell__section',
                    'sowGroupCell__section',
                    ) \
                .prefetch_related(
                    'sow_set__tour',
                    'sow_set__status',
                    'piglets__metatour__records__tour__sowfarrow_set',)
            serializer = LocationCellSerializer(data, many=True)
            print(serializer.data)

    def test_location_section_serializer_queries(self):
        with self.assertNumQueries(1):
            data = Location.objects.all() \
                .select_related(
                    'section__workshop',
                    ) 
            serializer = LocationSectionSerializer(data, many=True)
            print(serializer.data)


# class WorkshopModelTest(TestCase):
#     def setUp(self):
#         locations_testing.create_workshops_sections_and_cells()
#         sows_testing.create_statuses()
#         piglets_testing.create_piglets_statuses()