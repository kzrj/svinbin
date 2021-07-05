# -*- coding: utf-8 -*-
from datetime import timedelta, date, datetime
from freezegun import freeze_time

from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testings
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing

from piglets.models import Piglets
from piglets_events.models import Recount
from tours.models import Tour
from locations.models import Location


class ReportDateViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        piglets_testing.create_piglets_statuses()
        staff_testing.create_svinbin_users()

        self.brig8 = User.objects.get(username='brigadir8')
        self.admin = User.objects.get(username='test_admin1')
        self.shmigina = User.objects.get(username='shmigina')

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.locs_ws3 = Location.objects.filter(sowAndPigletsCell__isnull=False)
        self.locs_ws5 = Location.objects.filter(pigletsGroupCell__workshop__number=5)

        self.piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws3[0], 10)
        self.piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws5[0], 100)

    def test_all_ws_balance(self):
        with freeze_time("2021-02-25"):
            Recount.objects.create_recount(piglets=self.piglets1, new_quantity=12)
            Recount.objects.create_recount(piglets=self.piglets2, new_quantity=105)

        self.client.force_authenticate(self.shmigina)
        response = self.client.get('/api/reports/recounts/all_ws_balance/?start_date=2021-01-05')
        self.assertEqual(response.data[0]['recounts_balance_count'], 1)

    def test_detail_ws_balance(self):
        with freeze_time("2021-02-25"):
            Recount.objects.create_recount(piglets=self.piglets1, new_quantity=12)
            Recount.objects.create_recount(piglets=self.piglets2, new_quantity=105)

        self.client.force_authenticate(self.shmigina)
        response = self.client.get(
            '/api/reports/recounts/detail_ws_balance/?ws_number=3&start_date=2021-01-05')
        self.assertEqual(response.data[0]['number'], 6)
        self.assertEqual(response.data[0]['recounts'][0]['cell'], '6/45')
