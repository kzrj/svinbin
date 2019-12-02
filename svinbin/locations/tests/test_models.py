# -*- coding: utf-8 -*-
from django.test import TestCase, TransactionTestCase
from django.db import models

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing
import sows_events.utils as sows_events_testing

from locations.models import Location, WorkShop, Section, SowSingleCell, PigletsGroupCell, SowGroupCell, \
SowAndPigletsCell
from sows_events.models import SowFarrow
# from transactions.models import PigletsTransaction


class LocationModelManagerQuerysetTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        sows_events_testing.create_types()

    def test_queryset_with_all_related(self):
        sow1 = sows_testing.create_sow_seminated_usouded_ws3_section(1, 1)
        sow2 = sows_testing.create_sow_seminated_usouded_ws3_section(1, 1)
        sow3 = sows_testing.create_sow_seminated_usouded_ws3_section(2, 1)
        sow4 = sows_testing.create_sow_seminated_usouded_ws3_section(2, 2)
        sow5 = sows_testing.create_sow_seminated_usouded_ws3_section(1, 2)
        sow6 = sows_testing.create_sow_seminated_usouded_ws3_section(3, 3)
        SowFarrow.objects.create_sow_farrow(sow=sow1, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow2, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow3, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow4, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow5, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow6, alive_quantity=10)

        with self.assertNumQueries(3):
            data = Location.objects.all()\
                .select_related('section', 'workshop', 'pigletsGroupCell' ) \
                .prefetch_related('sow_set', 'piglets__metatour__records__tour',)
            print(data)

        with self.assertNumQueries(5):
            for location in data:
                piglets = location.piglets.all()
                for piglet in piglets:
                    print(piglet.metatour_repr)


class WorkshopModelTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
