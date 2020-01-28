# -*- coding: utf-8 -*-
from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ValidationError

from sows_events.models import (
    Semination, Ultrasound, SowFarrow, CullingSow,
    UltrasoundType, AbortionSow)
from sows.models import Sow, Boar
from piglets.models import Piglets
from locations.models import Location
from transactions.models import SowTransaction
from tours.models import Tour

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testing
import staff.testing_utils as staff_testings
import piglets.testing_utils as piglets_testing

from workshopthree.utils import reset_to_suporos


class UtilsTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_testing.create_boars()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()
        self.boar = Boar.objects.all().first()

    def test_reset_to_suporos(self):
        location = Location.objects.get(sowAndPigletsCell__section__number=4,
             sowAndPigletsCell__number=1)
        tour = Tour.objects.get_tour_by_week_in_current_year(1)
        piglets = piglets_testing.create_from_sow_farrow_by_week(week=1, location=location)

        sow = piglets.farrow.sow
        reset_to_suporos()

        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Супорос 35')
        self.assertEqual(sow.sowfarrow_set.all().count(), 0)

        location.refresh_from_db()
        self.assertEqual(location.is_piglets_empty, True)
