# -*- coding: utf-8 -*-
from django.test import TestCase

import locations.testing_utils as locaions_testing
import sows.testing_utils as sows_testings
import sows_events.utils as sows_events_testings
import staff.testing_utils as staff_testings

from staff.models import WorkShopEmployee


class WorkshopEmployeeManagerTest(TestCase):
    def setUp(self):
        locaions_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()

    def test_get_seminator_by_farm_name(self):
        shmigina = staff_testings.create_employee('ШМЫГИ')
        user = WorkShopEmployee.objects.get_seminator_by_farm_name('ШМЫГИ')
        self.assertEqual(user, shmigina)