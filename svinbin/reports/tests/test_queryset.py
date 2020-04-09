# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase, TransactionTestCase
from django.utils import timezone

from tours.models import Tour, MetaTour, MetaTourRecord
from sows.models import Sow
from sows_events.models import Semination, Ultrasound, SowFarrow
from locations.models import Location
from piglets.models import Piglets

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testing
import piglets.testing_utils as piglets_testing


class ReportTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        location1 = Location.objects.filter(sowAndPigletsCell__number=1).first()
        sow1 = sows_testing.create_sow_with_semination_usound(location=location1, week=1)
        farrow = SowFarrow.objects.create_sow_farrow(
            sow=sow1,
            alive_quantity=10,
            dead_quantity=0,
            mummy_quantity=0
            )

        location2 = Location.objects.filter(sowAndPigletsCell__isnull=False)[1]
        sow2 = sows_testing.create_sow_with_semination_usound(location=location2, week=1)
        farrow = SowFarrow.objects.create_sow_farrow(
            sow=sow2,
            alive_quantity=12,
            dead_quantity=5,
            mummy_quantity=1
            )

        location3 = Location.objects.filter(sowAndPigletsCell__isnull=False)[2]
        sow3 = sows_testing.create_sow_with_semination_usound(location=location3, week=1)
        farrow = SowFarrow.objects.create_sow_farrow(
            sow=sow3,
            alive_quantity=13,
            dead_quantity=3,
            mummy_quantity=2
            )

    def test_get_or_create_by_week_in_current_year(self):
        with self.assertNumQueries(1):
            sows = SowFarrow.objects.filter(tour__week_number=1)
            # print([sow for sow in sows])
            # bool(sows)
            # # print(sows)
            # print(sows[0])
            # print(sows[1])
            # print(sows)

            # sows.count_alive_piglets()
            # sows.count_dead_piglets()
            # sows.count_mummy_piglets()

            # print(sows.count_piglets_annotate()[0])
            sows = sows.count_piglets_by_tour_annotate()
            bool(sows)
            print(sows[0].total_alive)
            print(sows[0].total_dead)
            print(sows[0].total_mummy)

            # print(sows.count_alive_piglets_iterate())

