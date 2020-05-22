# -*- coding: utf-8 -*-
from datetime import timedelta, date
import copy

from django.utils import timezone

from rest_framework.test import APITestCase, APIClient

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testings
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing

from piglets.models import Piglets
from locations.models import Location
from tours.models import Tour, MetaTour
from reports.models import ReportDate, gen_operations_dict

from reports.serializers import ReportTourSerializer


class ReportDateViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        sows_events_testings.create_types()

        self.user = staff_testing.create_employee()
        self.client.force_authenticate(user=self.user)

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.loc_ws3_cells = Location.objects.filter(sowAndPigletsCell__isnull=False)

        self.ops_dict = gen_operations_dict()

        operations = dict()
        for op_key in self.ops_dict.keys():
            operations[op_key] = False

        self.request_json = {
            'operations': operations,
            'filters': {'start_date': None, 'end_date': None, 'farm_id': None},
            'target': None
        } 

    def test_report_date_view(self):
        response = self.client.get('/api/reports/director/')
        self.assertEqual(len(response.data['results']) > 0, True)

    def test_report_date_view(self):
        request_json = copy.deepcopy(self.request_json)
        request_json['operations']['ws1_semination'] = True

        response = self.client.post('/api/reports/operations/', request_json, format='json')
        print(response.data)
        # self.assertEqual(len(response.data['results']) > 0, True)